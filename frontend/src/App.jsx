import { Routes, Route } from "react-router-dom";
import Ads from "../src/Pages/Home/Ads";
import Nav from "../src/Pages/Home/Nav";
import Layout from "../src/Pages/Home/Layout/Layout";
import AboutUs from "../src/Pages/About/About";
import List from "./Pages/Sell/List";
import Footer from "./Pages/Home/Footer";
import SignUp from "./Pages/Auth/SignUp";
import SignIn from "./Pages/Auth/SignIn";
import ViewAll from "./Pages/Views/ViewAll";

const App = () => {
  return (
    <div>
      <Ads />
      <Nav />
      <Routes>
        <Route path="/" element={<Layout />} />
        <Route path="/list" element={<ViewAll />} />
        <Route path="/about-us" element={<AboutUs />} />
        <Route path="/Ongoing-Auction" element={<ViewAll />} />
        <Route path="/sign-up" element={<SignUp />} />
        <Route path="/sign-in" element={<SignIn />} />
      </Routes>
      <Footer />
    </div>
  );
};

export default App;
