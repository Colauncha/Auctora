import Button from "../../Components/Button";
import Search from "../../Components/Search";
import { email } from "../../Constants";

const Cta = () => {
  const handleEmailSubscription = () => {
    console.log("subscribed");
  };
  return (
    <div className="bg-gradient-to-r from-[#7B2334] to-[#9F3247] formatter rounded-md h-[320px] lg:h-[177px] py-[36px] px-[24px] md:px-[64px]">
      <div className="flex flex-col gap-8 lg:gap-0 lg:flex-row justify-between">
        <div className="text-[24px] font-[700] text-[#FFFFFF] lg:text-[40px]">
          STAY UP TO DATE ABOUT OUR LATEST AUCTIONS
        </div>
        <div className="flex flex-col gap-3">
          <Search
            img={email}
            placeholder={`Enter your email address`}
            onClick={handleEmailSubscription}
            className={`w-full h-[48px] lg:w-[350px] rounded-[25px]`}
          />
          <Button
            label={`Subscribe to Newsletter`}
            className={`border-[1px] text-red-800 bg-white outline-none border-none`}
          />
        </div>
      </div>
    </div>
  );
};

export default Cta;
