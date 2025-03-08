import { Routes, Route } from "react-router-dom";
import Ads from "../src/Pages/Home/Ads";
import Nav from "../src/Pages/Home/Nav";
import Layout from "../src/Pages/Home/Layout/Layout";
import AboutUs from "../src/Pages/About/About";
// import List from "./Pages/Sell/List";
import Footer from "./Pages/Home/Footer";
import SignUp from "./Pages/Auth/SignUp";
import SignIn from "./Pages/Auth/SignIn";
import ViewAll from "./Pages/Views/ViewAll";
import CategoryResult from "./Pages/Category/CategoryResult";
import DetailPage from "./Pages/Detail/Detail";

// verification pages
import Otp from "./Pages/Account/Otp";
import Profile from "./Pages/Dashboard/Profile";
import AddressVerification from "./Pages/Dashboard/AddressVerification";
import Notification from "./Pages/Notification/Notification";
import BankVerification from "./Pages/Dashboard/BankVerification";
import VerificationLoading from "./Pages/Dashboard/VerificationLoading";

// protected route
import ProtectedRoute from "./Pages/ProtectedRoute/ProtectedRoute";
// import GetStarted from "./Pages/Dashboard/GetStarted";
import AddProduct from "./Pages/Dashboard/AddProduct";
import ProductPhoto from "./Pages/Dashboard/AddProduct/ProductPhoto";
import Dashboard from "./Pages/Dashboard/Dashboard";

const App = () => {
  return (
    <div>
      <Ads />
      <Nav />
      <Routes>
        <Route path="/" element={<Layout />} />
        <Route path="/about-us" element={<AboutUs />} />
        <Route path="/category" element={<CategoryResult />} />
        <Route path="/category/:slug" element={<DetailPage />} />
        <Route path="/list" element={<ProductPhoto />} />
        <Route path="/notification" element={<Notification />} />
        <Route path="/Ongoing-Auction" element={<ViewAll />} />

        {/* Auth Routes */}
        <Route path="/sign-up" element={<SignUp />} />
        <Route path="/sign-in" element={<SignIn />} />

        {/* Verification Routes */}
        <Route path="/otp" element={<Otp />} />
        {/* complete logic for Otp and redirect to Profile */}
        <Route path="/profile" element={<Profile />} />
        <Route path="/address-verification" element={<AddressVerification />} />
        <Route path="/bank-verification" element={<BankVerification />} />
        <Route path="/verification-loading" element={<VerificationLoading />} />

        {/* Protected Routes */}
        <Route
          path="/dashboard"
          element={
            <ProtectedRoute>
              <Dashboard />
            </ProtectedRoute>
          }
        />
        <Route path="/add-product" element={<AddProduct />} />
      </Routes>
      <Footer />
    </div>
  );
};

export default App;
