import { google_auth } from "../../Constants";
import PropTypes from 'prop-types';
import Button from "../Button";
import Input from "./Input";
import useModeStore from "../../Store/Store";
import { useNavigate } from "react-router-dom";
import Loader from "../../assets/loader";
import {useState} from "react"
import useAuthStore from "../../Store/AuthStore";
import style from "./css/auth.module.css";
import { current } from "../../utils";

const AuthFormSginIn = ({ heading }) => {
  const { isMobile } = useModeStore();
  const navigate = useNavigate();

  // States of the applications
  const [email, setEmail] = useState("")
  const [password, setPassword] = useState("")
  // const [checked, setChecked] = useState(true)
  const [alertT, setAlert] = useState({isAlert: false, level: 'warn', message: ""});
  const [loading, setLoading]=useState(false)
  const login = useAuthStore((state) => state.login);

  const submit = async (e) => {
    e.preventDefault();
    setLoading(true);

    const data = {
      identifier: email,
      password
    }

    console.log(JSON.stringify(data))
    let endpoint = `${current}users/login`;

    try {
      const response = await fetch(endpoint, {
       method: "POST",
       headers: {
        'Content-Type':'application/json',
       },
       body: JSON.stringify(data),
       credentials: "include",
      });
      if (response.ok){
        const data = await response.json();
        console.log('Login Successful', data);
        localStorage.setItem('token', JSON.stringify(data.data.token));
        setAlert({isAlert: true, level: "success", message: "Log In Successful"})
        setTimeout(() => {
          login(data.data.token.split('.')[0])
          setLoading(false)
          navigate('/dashboard')
        }, 500)
      } else{
        const errorData = await response.json();
        console.error('Login Failed: ', errorData);
        setTimeout(() => {
          setLoading(false)
          setAlert({isAlert: true, message: `${errorData.message}: ${errorData.detail}`})
        }, 500)
      }
    } catch (error) {
      console.error('Error during Login', error)
      setTimeout(() => {
        setLoading(false)
        setAlert({isAlert: true, message: error.message})
      }, 500)
    }
  };

  const signUp = () => {
    navigate("/sign-up");
  };
  return (
    <div className="w-[620px] h-[500px] p-10 bg-white rounded-tl-md rounded-bl-md">
      <form >
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
          {isMobile && (
            <div className="flex items-center gap-1">
              <p className="text-[#848a8f] text-[12px]">
                Don&apos;t have an account?{" "}
              </p>
              <span
                className="text-[#de506d] text-[12px] cursor-pointer"
                onClick={signUp}
              >
                Sign Up
              </span>
            </div>
          )}
          <Input
            title={`Email`}
            id={`email`}
            value={email}
            type={`email`}
            htmlFor={`email`}
            className={`focus:outline-[#9f3248]`}
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
            value={password}
            className={`focus:outline-[#9f3248]`}
            onChange={(e) => {
              setAlert({isAlert: false, message: ""})
              setPassword(e.target.value)
            }}
          />

          {/* <div className="flex items-center  gap-4">
            <Input
              id={`checkbox`}
              type={`checkbox`}
              htmlFor={`checkbox`}
              className={`focus:outline-none`}
              value={checked}
              onChange={(e)=>setChecked(e.target.checked)}
            />
            <p className="text-[#848a8f]">Remember Me</p>
          </div> */}
          <Button
            label={`Login`}
            onClick={submit }
            className={`hover:bg-[#de506d]`}
            disabled={loading}
          >{loading ? "Submitting": "Logged IN"}</Button>
        </fieldset>
      </form>
      <div className="flex flex-col gap-3 mt-2 items-center">
        <p>Or Login with</p>
        <div className="flex items-center gap-3">
          <img src={google_auth} alt="" className="w-10 h-10 cursor-pointer" />
        </div>
      </div>
    </div>
  );
};
AuthFormSginIn.propTypes = {
  heading: PropTypes.string.isRequired,
};

export default AuthFormSginIn;
