import { fb_auth, google_auth, insta_auth } from "../../Constants";
import Button from "../Button";
import Input from "./Input";

const AuthFormSginUp = ({ heading }) => {
  const submit = () => {
    console.log("submitting....");
  };
  return (
    <div className="w-[620px] h-[500px] p-10 bg-white rounded-tl-md rounded-bl-md">
      <form action="">
        <fieldset className="flex flex-col gap-3">
          <legend className="text-[30px] font-[700] text-[#9f3247]">
            {heading}
          </legend>
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
          <Input
            title={`Confirm Password`}
            id={`password`}
            type={`password`}
            htmlFor={`password`}
          />
          <div className="flex items-center  gap-4">
            <Input
              id={`checkbox`}
              type={`checkbox`}
              htmlFor={`checkbox`}
              className={`outline-none border-none`}
            />
            <p className="text-[#848a8f]">I accept terms and conditions</p>
          </div>
          <Button
            label={`Register`}
            onClick={submit}
            className={`hover:bg-[#de506d]`}
          />
        </fieldset>
      </form>
      <div className="flex flex-col gap-3 mt-2 items-center">
        <p>Or sign Up With</p>
        <div className="flex items-center gap-3">
          <img src={google_auth} alt="" className="w-10 h-10" />
          <img src={fb_auth} alt="" className="w-10 h-10" />
          <img src={insta_auth} alt="" className="w-10 h-10" />
        </div>
      </div>
    </div>
  );
};

export default AuthFormSginUp;
