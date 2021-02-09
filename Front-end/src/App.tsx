import * as React from 'react';
import './App.css';
import { BrowserRouter as Router, Switch, Route } from 'react-router-dom';
import NavBar from './layout/navbar';
import Usage from './components/Usage';
import Printers from './components/Printers';
import Maintenance from './components/Maintenance';
import Configuration from './components/Configuration';
import NotFound from './components/NotFound';
import EditUsage from './components/EditUsage';
import EditPrinter from './components/EditPrinter';
import ViewUsage from './components/ViewUsage';
import AddPrinter from './components/AddPrinter';

// Function to load Navbar and to map the route URLs to components
function App() {

  return (
    <Router>
      <div className="App">
        <NavBar />
        <Switch>
          <Route exact path="/" component={Printers} />
          <Route exact path="/printers" component={Printers} />
          <Route exact path="/usage" component={Usage} />
          <Route exact path="/maintenance" component={Maintenance} />
          <Route exact path="/configuration" component={Configuration} />
          <Route exact path="/usage/edit/:id" component={EditUsage} />
          <Route exact path="/usage/:id" component={ViewUsage} />
          <Route exact path="/printer/edit/:id" component={EditPrinter} />
          <Route exact path="/printers/add" component={AddPrinter} />
          <Route component={NotFound} />
        </Switch>
      </div>
    </Router>
  );
}

export default App;
