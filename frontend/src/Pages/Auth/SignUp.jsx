import { useNavigate } from "react-router-dom";
import AuthNote from "../../Components/auth/AuthNote";
import Breadcrumbs from "../../Components/Breadcrumbs";
import Button from "../../Components/Button";
import AuthFormSginUp from "../../Components/auth/AuthFormSginUp";

const SignUp = () => {
  const navigage = useNavigate();
  const login = () => {
    navigage("/sign-in");
  };
  return (
    <div className="bg-[#F2F0F1] min-h-screen">
      <div className="formatter">
        <div className="py-6">
          <Breadcrumbs />
          <div className="flex w-full">
            <AuthFormSginUp heading={`Sign Up`} />
            <div className="hidden lg:block">
              <AuthNote
                heading={`Create Account`}
                body={`Create an account to dive into the world of auctions and unveil hidden treasures. As a member of Auctora, you'll gain exclusive access to bid on unique, one-of-a-kind items, from vintage gems to intriguing antiques. Don't miss out on the excitement – sign up now and embark on a journey where every bid is a step closer to uncovering extraordinary finds! Join the auction adventure today!
`}
                button={
                  <Button
                    label={`Already have an account? Login here`}
                    onClick={login}
                    className={`text-[14px] hover:bg-[#9f324865]`}
                  />
                }
              />
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default SignUp;
