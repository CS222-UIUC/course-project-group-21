import React from "react"

import { Nav, NavLink, NavMenu }
    from "./NavbarElements"

const Navbar = () => {
    return (
        <>
            <Nav>
                <NavMenu>
                    <NavLink to="home" activeStyle>
                        Home
                    </NavLink>
                    <NavLink to="american_beliefs" activeStyle>
                        American Climate Change Beliefs
                    </NavLink>
                    <NavLink to="arctic_ice" activeStyle>
                        Arctic Sea Ice
                    </NavLink>
                    <NavLink to="sea_levels" activeStyle>
                        Sea Level Predictions
                    </NavLink>
                    <NavLink to="warming_projections" activeStyle>
                        Warming Projections
                    </NavLink>
                    <NavLink to="fight_cc" activeStyle>
                        Fight Climate Change
                    </NavLink>
                    <NavLink to="carbon" activeStyle>
                        Carbon Emissions and Temperature
                    </NavLink>
                    <NavLink to="variables_cc" activeStyle>
                        Variables of Climate Change
                    </NavLink>
                </NavMenu>
            </Nav>
        </>
    );
};

export default Navbar;