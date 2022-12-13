import { FaBars } from "react-icons/fa";
import { NavLink as Link } from "react-router-dom";
import styled from "styled-components";

export const Nav = styled.nav`
font-family: 'Roboto';
background: #272b63;
align-items: center;
// text-align: center;
// border-radius: 7px;
height: 100px;
display: flex;
align: center;
justify-content: space-between;
z-index: 12;
`;

export const NavLink = styled(Link)`
align-items: center;
font-family: 'RobotoLight';
font-size: 20px;
color: #ffffff;
display: flex;
align-items: center;
text-decoration: none;
padding: 1rem;
height: 100%;
cursor: pointer;
&.active {
	color: #64eded;
	text-decoration: underline;
}
`;

export const Bars = styled(FaBars)`
font-family: 'Roboto';
display: none;
color: #808080;
@media screen and (max-width: 768px) {
	display: block;
	position: absolute;
	top: 0;
	right: 0;
	transform: translate(-100%, 75%);
	font-size: 1.8rem;
	cursor: pointer;
}
`;

export const NavMenu = styled.div`
font-family: 'Roboto';

display: flex;
align-items: center;
// margin-right: -24px;
/* Second Nav */
/* margin-right: 24px; */
/* Third Nav */
/* width: 100vw;
white-space: nowrap; */
@media screen and (max-width: 768px) {
	display: none;
}
`;
