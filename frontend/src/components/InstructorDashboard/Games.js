import React from 'react';
import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableHead from '@material-ui/core/TableHead';
import TableRow from '@material-ui/core/TableRow';
import CircularProgress from '@material-ui/core/CircularProgress';
import Title from './Title';
import CheckIcon from '@material-ui/icons/Check';
import axios from "axios";
import Cookies from 'js-cookie';

import { Container } from '@material-ui/core';

export default function Games() {
  const [loading, setLoading] = React.useState(true);
  const [games, setGames] = React.useState([]);

  // Executed when the Route is mounted. Empty Array is the second argument in order to execute once.
  React.useEffect(() => {
    axios.get('http://localhost:8086/instructor/games', {headers: {'SESSION-KEY': Cookies.get('SESSION-KEY')}})
    .then((response) => {
      setGames(response.data['games']);
      setLoading(false);
    })
    .catch((error) => {
      if (error.response) {
        console.log(error.response);
      }
    })
  }, [])

  const tableBody = (rows) => (<TableBody>
          {rows.map((row) => (
            <TableRow key={row.id}>
              <TableCell>{row.id}</TableCell>
              <TableCell>{row.active ? <CheckIcon/> : <div/>}</TableCell>
              <TableCell>{row.wholesaler_present ? <CheckIcon/> : <div/>}</TableCell>
              <TableCell>{row.retailer_present ? <CheckIcon/> : <div/>}</TableCell>
              <TableCell>{row.holding_cost}</TableCell>
              <TableCell>{row.backlog_cost}</TableCell>
              <TableCell>{row.session_length}</TableCell>
            </TableRow>
          ))}
        </TableBody>)

  return (
    <React.Fragment>
      {loading ? <CircularProgress/> :
      <Container>
      <Title>Recent Games</Title>
      <Table size="small">
        <TableHead>
          <TableRow>
            <TableCell>ID</TableCell>
            <TableCell>Active</TableCell>
            <TableCell>Wholesaler</TableCell>
            <TableCell>Retailer</TableCell>
            <TableCell>Holding Cost</TableCell>
            <TableCell>Backlog Cost</TableCell>
            <TableCell>Session Length</TableCell>
          </TableRow>
        </TableHead>
        {tableBody(games)}
      </Table>
      </Container>
      }
    </React.Fragment>
  );
}
