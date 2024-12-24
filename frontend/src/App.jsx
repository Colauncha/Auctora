import { Routes, Route } from "react-router-dom";
import Ads from "../src/Pages/Home/Ads";
import Nav from "../src/Pages/Home/Nav";
import Layout from "../src/Pages/Home/Layout/Layout";
import AboutUs from "../src/Pages/About/About";
import Footer from "./Pages/Home/Footer";
import SignUp from "./Pages/Auth/SignUp";
import SignIn from "./Pages/Auth/SignIn";
<<<<<<< Updated upstream
=======
import ViewAll from "./Pages/Views/ViewAll";
import Bid from "./Pages/Bid/Bid";
>>>>>>> Stashed changes

const App = () => {
  return (
    <div>
      <Ads />
      <Nav />
      <Routes>
        <Route path="/" element={<Layout />} />
        <Route path="/list" element={<List />} />
        <Route path="/about-us" element={<AboutUs />} />
<<<<<<< Updated upstream
        <Route path="sign-up" element={<SignUp />} />
        <Route path="sign-in" element={<SignIn />} />
=======
        <Route path="/Ongoing-Auction" element={<ViewAll />} />
        <Route path="/sign-up" element={<SignUp />} />
        <Route path="/sign-in" element={<SignIn />} />
        <Route path="/bid" element={<Bid />} />
>>>>>>> Stashed changes
      </Routes>
      <Footer />
    </div>
  );
};

export default App;
