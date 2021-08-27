import React, { useState, useEffect } from 'react';
import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableHead from '@material-ui/core/TableHead';
import TableRow from '@material-ui/core/TableRow';
import TableContainer from '@material-ui/core/TableContainer';
import Title from './Title';
import CheckIcon from '@material-ui/icons/Check';
import ClearIcon from '@material-ui/icons/Clear';
import TextField from '@material-ui/core/TextField';
import Box from '@material-ui/core/Box';
import Button from '@material-ui/core/Button';

import Game from "../../models/Game";
import GameState from "../../models/GameState";
import { Grid, Paper, makeStyles, CircularProgress } from '@material-ui/core';
import axios from 'axios';
import Cookies from 'js-cookie';

const useStyles = makeStyles((theme) => ({
  root: {
    flexGrow: 1,
    padding: 15,
  },
  
  paper: {
    height: 140,
    width: 100,
  },
  
  control: {
    padding: theme.spacing(2),
  },
  
  inputDesc: {
    margin: 20,
  },
  
  table: {
    border: '1px solid #eee',
  },
  
  tableRight: {
    borderLeft: 'none',
  },
  
  additionalInfo: {
    margin: '20px 0 0',
  },
  
  head: {
    backgroundColor: '#dadada',
  },
  
  plotButtonGroup: {
    margin: '20px auto',
  },
  
  plotButton: {
    margin: '0 10px',
  },

  experimental: {
    width: '100%',
    height: '300px',
    backgroundColor: '#000',
  }

}));

export default function CurrentGame() {

  const [game, setGame] = useState();
  const [game_state, setGameState] = useState();
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    axios.get('http://localhost:8086/player/game', { headers: {'SESSION-KEY': Cookies.get('SESSION-KEY')} })
      .then((response) => {
        if (response.data.game) {
          setGame(response.data.game);
          setGameState(response.data.game_state);
          setLoading(false);
        } else {
          alert('No valid game state found, please join a game!');
        }
      });
  }, [])

  const [units, setUnits] = useState({
    purchase_units: 0,
  });

  const purchaseUnits = (e) => {
    console.log(units);
    e.preventDefault();
    axios.post('http://localhost:8086/player/game/play', units, {headers: {'SESSION-KEY': Cookies.get('SESSION-KEY')}})
    .then((response) => {
      
      alert("Order entered successfully! Units ordered: " + units.purchase_units);
      window.location.reload(false);
    })
    .catch((error) => {
        if (error.response) {
          alert('Failed to enter data: ' + error.response.status);
        } 
        else if (error.request) {
          alert('Bad request');
        }
      });
  }

  const handleChange = (e) => {
    const { name, value, type } = e.target

    setUnits(prevUnits => ({
      ...prevUnits,
      [name]: type === 'number' ? parseInt(value) : value
    }))
  }

  const classes = useStyles();
  return (
    <React.Fragment>
      {loading ? <CircularProgress /> : 

        <div>
        <Grid container className={classes.root} spacing={2}>
          <Grid item xs={12}>
            <Paper variant="outlined">
              <Title>Current Game</Title>
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
                <TableBody>
                  <TableRow key={game.id}>
                    <TableCell>{game.id}</TableCell>
                    <TableCell>{game.active ? <CheckIcon /> : <div />}</TableCell>
                    <TableCell>{game.wholesaler_present ? <CheckIcon /> : <div />}</TableCell>
                    <TableCell>{game.retailer_present ? <CheckIcon /> : <div />}</TableCell>
                    <TableCell>{game.holding_cost}</TableCell>
                    <TableCell>{game.backlog_cost}</TableCell>
                    <TableCell>{game.session_length}</TableCell>
                  </TableRow>
                </TableBody>
              </Table>

            </Paper>
          </Grid>


          <Grid item xs={6}>
            <Paper variant="outlined">
              <Title>
                Input Screen for <b>{game_state.role}</b> of Game {game.id}
              </Title>
              <p>For Week {game_state.week}</p>

              <Box display="flex" flexDirection="row">
                <TableContainer className={classes.tableBorder}>
                  <Table className={classes.table} aria-label="caption table">

                    <TableHead>
                      <TableRow>
                        <TableCell>Demand from <b>{game_state.supplier}</b>:</TableCell>
                        <TableCell align="right">{game_state.incoming_orders}</TableCell>
                      </TableRow>
                    </TableHead>

                    <TableBody>
                        <TableRow>
                          <TableCell>On backorder</TableCell>
                          <TableCell align="right">{game_state.backorder}</TableCell>
                        </TableRow>

                        <TableRow>
                          <TableCell>Total requirements</TableCell>
                          <TableCell align="right">{game_state.total_requirement}</TableCell>
                        </TableRow>
                    </TableBody>
                  </Table>
                </TableContainer>

                <TableContainer className={classes.tableBorder}>
                  <Table className={classes.table} aria-label="caption table">
                    <TableHead>
                      <TableRow>
                        <TableCell>Beginning Inventory</TableCell>
                        <TableCell align="right">{game_state.inventory}</TableCell>
                      </TableRow>
                    </TableHead>
                    <TableBody>
                      
                        <TableRow>
                          <TableCell>Incoming Shipment</TableCell>
                          <TableCell align="right">{game_state.shipment}</TableCell>
                        </TableRow>

                        <TableRow>
                          <TableCell>Total available</TableCell>
                          <TableCell align="right">{game_state.total_inventory}</TableCell>
                        </TableRow>
      
                    </TableBody>
                  </Table>
                </TableContainer>
              </Box>

              <Box className={classes.additionalInfo}>
                <p>Units shipped to retailer last week: {game_state.unit_shipped}</p>
                <p>Ending inventory: {game_state.ending_inventory}</p>
              </Box>
                
              
                <form className={classes.root} noValidate autoComplete="off">                 
                  {game_state.can_play ?
                    <div>
                    {/* User is allowed to enter the data */}
                      <Box display="flex" justifyContent="center" alignItems="center">
                        <p className={classes.inputDesc}>Enter the number to be purchased: </p>
                        <TextField 
                          name="purchase_units"
                          type="number"
                          value={units.purchase_units}
                          onChange={handleChange}

                          label="Order"
                          id="outlined-size-small"
                          variant="outlined"
                          size="small"
                        />
                      </Box>

                      <Button type="submit" variant="contained" color="primary" onClick={purchaseUnits} disableElevation>
                        Submit
                      </Button>
                    </div>

                    :

                    <div>
                      {/* User is NOT allowed to enter the data */}
                      <Box display="flex" justifyContent="center" alignItems="center">
                        <p className={classes.inputDesc}>Enter the number to be purchased: </p>
                        <TextField 
                          name="purchase_units"
                          type="number"
                          value={units.purchase_units}
                          onChange={handleChange}

                          label="Order"
                          id="outlined-size-small"
                          variant="outlined"
                          size="small"

                          disabled
                        />
                      </Box>
                      
                      <Button type="submit" variant="contained" color="primary" onClick={purchaseUnits} disabled disableElevation>
                        Submit
                      </Button>
                    </div>
                  }
                  
                </form>
              
                

            </Paper>
          </Grid>

          <Grid item xs={6}>
            <Paper variant="outlined">
              <Title>
                <b>{game_state.role}</b> information for the  last 10 weeks
              </Title>

              <Box display="flex" flexDirection="row">
                <TableContainer className={classes.tableBorder}>
                  <Table className={classes.table} aria-label="caption table">

                    <TableHead className={classes.head}>
                      <TableRow>
                        <TableCell>Week</TableCell>
                        <TableCell>Inv/Bk</TableCell>
                        <TableCell>Demand</TableCell>
                        <TableCell>Inc. ship.</TableCell>
                        <TableCell>Outg. ship.</TableCell>
                        <TableCell>Order placed</TableCell>
                        <TableCell>Current Cost</TableCell>
                      </TableRow>
                    </TableHead>

                    <TableBody>
                        <TableRow>
                          <TableCell align="center">0</TableCell>
                          <TableCell align="center">0</TableCell>
                          <TableCell align="center">0</TableCell>
                          <TableCell align="center">0</TableCell>
                          <TableCell align="center">0</TableCell>
                          <TableCell align="center">0</TableCell>
                          <TableCell align="center">0</TableCell>
                        </TableRow>
                    </TableBody>
                  </Table>
                </TableContainer>

              </Box>
            </Paper>
          </Grid>


          <Grid item xs={12}>
            <Paper variant="outlined">
              <Title>Game State</Title>
              {/* TODO: Add periodic timer for status update */}
              <p>Status will be updated in N seconds</p>
              <Table size="small">
                <TableHead>
                  <TableRow>
                    <TableCell>Factory</TableCell>
                    <TableCell>Distributor</TableCell>
                    <TableCell>Wholesaler</TableCell>
                    <TableCell>Retailer</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  <TableRow key={game.id}>
                    {/*TODO: Checks for players' readyness*/}
                    <TableCell><ClearIcon/></TableCell>
                    <TableCell>{game.active ? <CheckIcon /> : <ClearIcon />}</TableCell>
                    <TableCell>{game.wholesaler_present ? <CheckIcon /> : <ClearIcon />}</TableCell>
                    <TableCell>{game.retailer_present ? <CheckIcon /> : <ClearIcon />}</TableCell>
                  </TableRow>
                </TableBody>
              </Table>

              <Box className={classes.plotButtonGroup} display="flex" flexDirection="row" justifyContent="center" alignItems="center">
                <Button variant="contained" className={classes.plotButton} color="primary" disableElevation>
                  Demand Plot
                </Button>
                <Button variant="contained" className={classes.plotButton} color="primary" disableElevation>
                  Order Plot
                </Button>
                <Button variant="contained" className={classes.plotButton} color="primary" disableElevation>
                  Inv/Backorder Plot
                </Button>
                <Button variant="contained" className={classes.plotButton} color="primary" disableElevation>
                  Plot All
                </Button>
              </Box>
            </Paper>
          </Grid>
        </Grid>
        </div>
      }
    </React.Fragment>
  );
}
