import React from 'react';
import Cookies from 'js-cookie';
import InstructorDashboard from './InstructorDashboard/Dashboard';
import PlayerDashboard from './PlayerDashboard/Dashboard';

// Determines which dashboard to render based on the user's role.
export default function Dashboard() {

    return (Cookies.get('role') === 'instructor' ? <InstructorDashboard/> : <PlayerDashboard/>);
}