import { Button, makeStyles, TextField, FormControlLabel, FormGroup, FormControl, Switch, InputLabel, Select, MenuItem, Grid } from '@material-ui/core';
import React, {useState} from 'react';
import Cookies from 'js-cookie';
import axios from "axios";

const useStyles = makeStyles((theme) => ({
  paper: {
    marginTop: theme.spacing(8),
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
  },
  avatar: {
    margin: theme.spacing(1),
    backgroundColor: theme.palette.secondary.main,
  },
  form: {
    width: '100%', // Fix IE 11 issue.
    marginTop: theme.spacing(1),
  },
  formControl: {
    margin: theme.spacing(1),
    minWidth: 200,
  },
  submit: {
    margin: theme.spacing(3, 0, 2),
  },
}));


function CreateGame() {

  const [state, setState] = useState({
        session_length: 20,
        wholesaler_present: true,
        retailer_present: true,
        info_sharing: true,
        demand_pattern_id: 1,
        info_delay: 3,
        holding_cost: 10,
        backlog_cost: 10,
        });

    const patterns = [1,2,3,4];

    //this function handles all the changes made to the state variables
    const handleChange = (e) => {
        const { name, value, type } = e.target
        setState(prevState => ({
            ...prevState,
            [name]: type === "number" ? parseInt(value, 10) : value
        }))
    }

    const handleSwitchChange = (e) => {
        const { name, checked } = e.target
        setState(prevState => ({
            ...prevState,
            [name]: checked
        }))
    }

    const createGame = (e) => {
      e.preventDefault();
      console.log(state);
      axios.post('http://localhost:8086/instructor/game', state, {headers: {'SESSION-KEY': Cookies.get('SESSION-KEY')}})
      .then((response) => {
        console.log(response.data);
        alert("Game Created, id: " + response.data['game_id']);
      })
      .catch((error) => {
        if (error.response) {
          alert('Failed to create game, error code: ' + error.response.status);
        } 
        else if (error.request) {
          alert('Bad request');
        }
      });

    }

  const classes = useStyles();
  return (
    <Grid container spacing={2} direction="column" alignItems="flex-start">
      <FormControl>
        <Grid item>
          <TextField required name="session_length" type="number" className={classes.form} label="Session Length" value={state.session_length} onChange={handleChange}/>
          <TextField required name="info_delay" type="number" className={classes.form} label="Information Delay" value={state.info_delay} onChange={handleChange}/>
          <TextField required name="holding_cost" type="number" className={classes.form} label="Holding Cost" value={state.holding_cost} onChange={handleChange}/>
          <TextField required name="backlog_cost" type="number" className={classes.form} label="Backlog Cost" value={state.backlog_cost} onChange={handleChange}/>
        </Grid>
        <Grid item>
        <FormGroup row>
          <FormControlLabel label="Wholesaler"
          control={
            <Switch
              checked={state.wholesaler_present}
              onChange={handleSwitchChange}
              name="wholesaler_present"
              color="primary"
            />
          }/>
          <FormControlLabel label="Retailer"
          control={<Switch
              checked={state.retailer_present}
              onChange={handleSwitchChange}
              name="retailer_present"
              color="primary"
            />
          }/>
          <FormControlLabel label="Information Sharing"
          control={<Switch
              checked={state.info_sharing}
              onChange={handleSwitchChange}
              name="info_sharing"
              color="primary"
            />
          }/>
        </FormGroup>
        </Grid>
        </FormControl>
        <Grid item>
          <FormControl className={classes.formControl}>
          <InputLabel id="pattern_label">Demand Pattern</InputLabel>
          <Select labelId="pattern_label" name="demand_pattern_id" value={state.demand_pattern_id} onChange={handleChange}>
            {patterns.map((pattern_id) => (<MenuItem value={pattern_id} key={pattern_id}>{pattern_id}</MenuItem>))}
          </Select>
          </FormControl>
        </Grid>
        <Grid item>
          <Button variant="contained" color="primary" onClick={createGame}>
            Create Game
          </Button>
        </Grid>
    </Grid>
  );

}

export default CreateGame;