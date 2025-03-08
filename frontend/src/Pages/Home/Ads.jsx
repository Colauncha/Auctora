import Button from "../../Components/Button";
import { useNavigate } from "react-router-dom";
import useAuthStore from "../../Store/AuthStore";

const Ads = () => {
  const navigate = useNavigate();
  const isAuthenticated = useAuthStore((state) => state.isAuthenticated);
  
  const signup = () => {
    navigate("/sign-up", { state: { referrer: "Hompage" } });
  };
  return (
    <div className=" bg-gradient-to-r from-[#7B2334] to-[#9F3247] h-[38px] w-full md:max-w-[1433px] flex items-center justify-center gap-0 text-[12px] md:text-[14px]">
      {isAuthenticated ? (
        <p className="text-white">
          Welcome to Auctora
        </p>
      ) : (
      <>
        <p className="text-white">Sign up and get your first order.</p>
          <Button
            label="Sign Up Now"
            className="text-white bg-transparent"
            onClick={signup}
          />
        </>
      )}
    </div>
  );
};

export default Ads;
