import { fb_auth, google_auth, insta_auth } from "../../Constants";
import Button from "../Button";
import Input from "./Input";
import useModeStore from "../../Store/Store";
import { useNavigate } from "react-router-dom";
import {useState, useEffect} from "react"

const AuthFormSginIn = ({ heading }) => {
  const { isMobile } = useModeStore();
  const navigate = useNavigate();
  // States of the applications
  const [email, setEmail] = useState("")
  const [password, setPassword] = useState("")
  const [checked, setChecked] = useState(false)
  const [loading, setLoading]=useState(false)


  const submit = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      const response = await fetch('http://localhost:5000/api/login', {
       method: "POST",
       headers: {
        'Content-Type':'applications/json',
       },
       body:JSON.stringify({email, password}),
      });
      if (response.ok){
        const data = await response.json();
        console.log('Login Successful', data);
        localStorage.setItem('token', data.token);
        alert('Login Successful')
        navigate('/add-product') // add product
      } else{
        const errorData = await response.json();
        console.error('Login Failed: ', errorData.message);
        
      }
    } catch (error) {
      console.error('Error during Login', error)
    } finally{
      setLoading(false)
    }
    console.log("Logging in, please wait");
  };
  const signUp = () => {
    navigate("/sign-up");
  };
  return (
    <div className="w-[620px] h-[500px] p-10 bg-white rounded-tl-md rounded-bl-md">
      <form >
        <fieldset className="flex flex-col gap-3">
          <legend className="text-[30px] font-[700] text-[#9f3247]">
            {heading}
          </legend>
          {isMobile && (
            <div className="flex items-center gap-1">
              <p className="text-[#848a8f] text-[12px]">
                Don't have an account?{" "}
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
            onChange={(e)=>setEmail(e.target.value)}
          />
          <Input
            title={`Password`}
            id={`password`}
            type={`password`}
            htmlFor={`password`}
            value={password}
            className={`focus:outline-[#9f3248]`}
            onChange={(e)=>setPassword(e.target.value)}
          />

          <div className="flex items-center  gap-4">
            <Input
              id={`checkbox`}
              type={`checkbox`}
              htmlFor={`checkbox`}
              className={`focus:outline-none`}
              value={checked}
              onChange={(e)=>setChecked(e.target.checked)}
            />
            <p className="text-[#848a8f]">Remember Me</p>
          </div>
          <Button
            label={`Login`}
            onClick={submit}
            className={`hover:bg-[#de506d]`}
            disabled={loading}
          >{loading ? "Submitting": "Logged IN"}</Button>
        </fieldset>
      </form>
      <div className="flex flex-col gap-3 mt-2 items-center">
        <p>Or Login with</p>
        <div className="flex items-center gap-3">
          <img src={google_auth} alt="" className="w-10 h-10 cursor-pointer" />
          <img src={fb_auth} alt="" className="w-10 h-10 cursor-pointer" />
          <img src={insta_auth} alt="" className="w-10 h-10 cursor-pointer" />
        </div>
      </div>
    </div>
  );
};

export default AuthFormSginIn;
