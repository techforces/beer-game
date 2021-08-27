import { Button, makeStyles, TextField, FormControl, Grid, InputLabel, Select, MenuItem} from '@material-ui/core';
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


function JoinGame() {

  const roles = ['factory','distributor','retailer','wholesaler']

  const [state, setState] = useState({
        game_id: null,
        game_role: roles[0],
        });


    //this function handles all the changes made to the state variables
    const handleChange = (e) => {
        const { name, value, type } = e.target
        setState(prevState => ({
            ...prevState,
            [name]: type === 'number' ? parseInt(value) : value
        }))
    }

    const joinGame = (e) => {
      e.preventDefault();
      console.log(state);
      axios.post('http://localhost:8086/player/join', state, {headers: {'SESSION-KEY': Cookies.get('SESSION-KEY')}})
      .then((response) => {
        console.log(response.data);
        alert("Joined game");
      })
      .catch((error) => {
        if (error.response) {
          alert('Failed to join game, error code: ' + error.response.status);
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
          <TextField required name="game_id" type="number" className={classes.form} label="Game Code" value={state.session_length} onChange={handleChange}/>
        </Grid>
        <Grid item>
          <FormControl className={classes.formControl}>
          <InputLabel id="role_label">Role</InputLabel>
          <Select labelId="role_label" name="game_role" value={state.game_role} onChange={handleChange}>
            {roles.map((role_name) => (<MenuItem value={role_name} key={role_name}>{role_name}</MenuItem>))}
          </Select>
          </FormControl>
        </Grid>
        <Grid item>
          <Button variant="contained" className={classes.submit} color="primary" onClick={joinGame}>
            Join Game
          </Button>
        </Grid>
      </FormControl>
    </Grid>
  );

}

export default JoinGame;