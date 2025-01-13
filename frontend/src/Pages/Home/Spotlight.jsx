import CountDown from "../../Components/CountDown";
import Carousel from "../../Components/Carousel";

const Spotlight = () => {
  return (
    <div className="bg-[#F2F0F1] min-h-screen lg:h-screen max-w-[1433px]">
      <div className="formatter flex flex-col lg:flex-row justify-between">
        <CountDown />
        <Carousel />
      </div>
    </div>
  );
};

export default Spotlight;
