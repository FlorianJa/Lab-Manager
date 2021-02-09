import React from 'react'
import { Link, NavLink } from 'react-router-dom'

/* Navbar component conntaining links to pages*/
const NavBar: React.FC = () => {
    return (
        <nav className="navbar navbar-expand-lg navbar-dark bg-primary">
            <div className="container">
                <Link className="navbar-brand" to="/printers">
                    <i className="material-icons md-30">
                        home
                    </i>
                </Link>
                <button
                    className="navbar-toggler"
                    type="button"
                    data-toggle="collapse"
                    data-target="#navbarSupportedContent"
                    aria-controls="navbarSupportedContent"
                    aria-expanded="false"
                    aria-label="Toggle navigation"
                >
                    <span className="navbar-toggler-icon"></span>
                </button>

                <div className="collapse navbar-collapse">
                    <ul className="navbar-nav ml-auto">
                        <li className="nav-item">
                            <NavLink className="nav-link" exact to="/printers">
                                Home
                  </NavLink>
                        </li>
                        <li className="nav-item">
                            <NavLink className="nav-link" exact to="/usage">
                                Usage
                  </NavLink>
                        </li>
                        <li className="nav-item">
                            <NavLink className="nav-link" exact to="/maintenance">
                                Maintenance
                  </NavLink>
                        </li>
                        <li className="nav-item">
                            <NavLink className="nav-link" exact to="/configuration">
                                Configuration
                  </NavLink>
                        </li>
                    </ul>
                </div>
            </div>
        </nav>
    );
};

export default NavBar