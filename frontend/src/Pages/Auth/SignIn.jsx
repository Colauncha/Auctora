import { useNavigate } from "react-router-dom";
import AuthNote from "../../Components/auth/AuthNote";
import Breadcrumbs from "../../Components/Breadcrumbs";
import Button from "../../Components/Button";
import AuthFormSginIn from "../../Components/auth/AuthFormSginIn";

const SignIn = () => {
  const navigate = useNavigate();
  const createAccount = () => {
    navigate("/sign-up");
  };
  return (
    <div className="bg-[#F2F0F1] min-h-screen">
      <div className="formatter">
        <div className="py-6">
          <Breadcrumbs />
          <div className="flex w-full">
            <AuthFormSginIn heading={`Sign In`} />
            <div className="hidden lg:block">
              <AuthNote
                heading={`Welcome back!`}
                body={`Welcome back! We're thrilled to see you again. Log in to Auctora and resume your journey into the world of exclusive auctions. Your next winning bid could be just a click away. Happy bidding!`}
                button={
                  <Button
                    label={`Don’t have an account? Signup here`}
                    onClick={createAccount}
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

export default SignIn;
