import { fb_auth, google_auth, insta_auth } from "../../Constants";
import Button from "../Button";
import Input from "./Input";
import useModeStore from "../../Store/Store";
import { useNavigate } from "react-router-dom";

const AuthFormSginIn = ({ heading }) => {
  const { isMobile } = useModeStore();
  const navigate = useNavigate();
  const submit = () => {
    console.log("submitting....");
  };
  const signUp = () => {
    navigate("/sign-up");
  };
  return (
    <div className="w-[620px] h-[500px] p-10 bg-white rounded-tl-md rounded-bl-md">
      <form action="">
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
            type={`email`}
            htmlFor={`email`}
          />
          <Input
            title={`Password`}
            id={`password`}
            type={`password`}
            htmlFor={`password`}
          />

          <div className="flex items-center  gap-4">
            <Input
              id={`checkbox`}
              type={`checkbox`}
              htmlFor={`checkbox`}
              className={`outline-none border-none focus:border-none`}
            />
            <p className="text-[#848a8f]">Remember Me</p>
          </div>
          <Button
            label={`Login`}
            onClick={submit}
            className={`hover:bg-[#de506d]`}
          />
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
