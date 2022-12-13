import React from "react";
import "./App.css";
import Navbar from "./components/Navbar";
import { BrowserRouter as Router, Routes, Route }
	from "react-router-dom";
import Home from "./pages/index";
import Ice from "./pages/arctic_ice";
import Beliefs from "./pages/american_beliefs";
import Sea from "./pages/sea_level";
import Fight from "./pages/fight_cc";
import Temperatures from "./pages/warming_projections";
import Carbon from "./pages/carbon";
import Variables from "./pages/variables_cc";

function App() {

	return (
		<Router>
			<Navbar />
			<Routes>
				<Route exact path="/home" element={<Home />} />
				<Route path='/arctic_ice' element={<Ice />} />
				<Route path='/american_beliefs' element={<Beliefs />} />
				<Route path='/sea_levels' element={<Sea />} />
				<Route path='/fight_cc' element={<Fight />} />
				<Route path='/warming_projections' element={<Temperatures />} />
				<Route path='/carbon' element={<Carbon />} />
				<Route path='/variables_cc' element={<Variables />} />
			</Routes>
		</Router>
	);
}

export default App;

