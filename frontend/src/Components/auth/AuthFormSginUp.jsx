import { google_auth } from "../../Constants";
import Button from "../Button";
import PropTypes from 'prop-types';
import Input from "./Input";
import useModeStore from "../../Store/Store";
import { useNavigate } from "react-router-dom";
import { useState } from "react";
import Loader from "../../assets/loader";
import style from "./css/auth.module.css";
import { current } from "../../utils";

const AuthFormSginUp = ({ heading }) => {
  const { isMobile } = useModeStore();
  const navigate = useNavigate();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPass, setConfirmPass] = useState("");
  const [alertT, setAlert] = useState({isAlert: false, level: 'warn', message: ""});
  const [checked, setChecked] = useState(false);
  const [loading, setLoading] = useState(false);

  const submit = async (e) => {
    e.preventDefault();
    setLoading(true);
    let endpoint = `${current}users/register`;

    if (password !== confirmPass) {
      setTimeout(() => {
        setAlert({ isAlert: true, message: "Passwords do not match" })
        setLoading(false)
      }, 500)
      return
    }
    try {
      const response = await fetch(endpoint, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ email, password }),
      });
      if (response.ok) {
        const data = await response.json();
        console.log("Sign Up Successful", data);
        setAlert({isAlert: true, level: "success", message: "Sign Up Successful"})
        setTimeout(() => {
          setLoading(false)
          navigate("/otp")
        }, 500)
      } else {
        const errorData = await response.json();
        console.error("sign up failed: ", errorData);
        setTimeout(() => {
          setLoading(false)
          setAlert({isAlert: true, message: `${errorData.message}: ${errorData.detail}`})
      }, 500)
      }
    } catch (error) {
      console.error("Error during sign up", error);
      setTimeout(() => {
        setLoading(false)
        setAlert({isAlert: true, message: error.detail})
      }, 500)
    }
  };
  const SignIn = () => {
    navigate("/sign-in");
  };
  return (
    <div className="w-[620px] h-[500px] p-10 bg-white rounded-tl-md rounded-bl-md">
      <form action="">
        {loading && <Loader />}
        <div className={
          `${alertT.isAlert ? style.alertShow : style.alertNone}
           ${alertT.level === 'success' ? style.alertSuccess : ''}
          `
          }>{alertT.message}</div>
        <fieldset className="flex flex-col gap-3">
          <legend className="text-[30px] font-[700] text-[#9f3247]">
            {heading}
          </legend>
          {/* Only on Mobile */}
          {isMobile && (
            <div className="flex items-center gap-1">
              <p className="text-[#848a8f] text-[12px]">
                Already have Account?
              </p>
              <span
                className="text-[#de506d] text-[12px] cursor-pointer"
                onClick={SignIn}
              >
                Sign In
              </span>
            </div>
          )}
          <Input
            title={`Email`}
            id={`email`}
            type={`email`}
            htmlFor={`email`}
            className={`focus:outline-[#9f3248]`}
            value={email}
            onChange={(e) => {
              setAlert({isAlert: false, message: ""})
              setEmail(e.target.value)
            }}
          />
          <Input
            title={`Password`}
            id={`password`}
            type={`password`}
            htmlFor={`password`}
            className={`focus:outline-[#9f3248]`}
            value={password}
            onChange={(e) => {
              setAlert({isAlert: false, message: ""})
              setPassword(e.target.value)
            }}
          />
          <Input
            title={`Confirm Password`}
            id={`confirmPass`}
            type={`password`}
            htmlFor={`password`}
            className={`focus:outline-[#9f3248]`}
            value={confirmPass}
            onChange={(e) => {
              setAlert({isAlert: false, message: ""})
              setConfirmPass(e.target.value)
            }}
          />
          <div className="flex items-center  gap-4">
            <Input
              id={`checkbox`}
              type={`checkbox`}
              htmlFor={`checkbox`}
              className={`outline-none border-none`}
              value={checked}
              onChange={(e) => setChecked(e.target.value)}
            />
            <p className="text-[#848a8f]">I accept terms and conditions</p>
          </div>
          <Button
            label={`Register`}
            onClick={submit}
            className={`hover:bg-[#de506d]`}
            >{loading ? "Submitting": "Logged IN"}</Button>
        </fieldset>
      </form>
      <div className="flex flex-col gap-3 mt-2 items-center">
        <p>Or sign Up With</p>
        <div className="flex items-center gap-3">
          <img src={google_auth} alt="" className="w-10 h-10" />
        </div>
      </div>
    </div>
  );
};

AuthFormSginUp.propTypes = {
  heading: PropTypes.string.isRequired,
};

export default AuthFormSginUp;
