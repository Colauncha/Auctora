import Button from "../../Components/Button";
import { useLocation, useNavigate } from "react-router-dom";

const Ads = () => {
  const navigate = useNavigate();

  const signup = () => {
    navigate("/sign-up", { state: { referrer: "Hompage" } });
  };
  return (
    <div className=" bg-gradient-to-r from-[#7B2334] to-[#9F3247] h-[38px] w-full md:max-w-[1433px] flex items-center justify-center gap-0 text-[12px] md:text-[14px]">
      <p className="text-white">Sign up and get your first order.</p>
      <Button
        label="Sign Up Now"
        className="text-white bg-transparent"
        onClick={signup}
      />
    </div>
  );
};

export default Ads;
