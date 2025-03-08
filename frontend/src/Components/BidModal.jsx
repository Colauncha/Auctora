import Button from "./Button";
import Input from "./auth/Input";

const BidModal = () => {
  return (
    <div className="flex flex-col h-[302px] gap-5">
      <h2 className="text-2xl font-bold">Place your Bid</h2>
      <div>time left</div>
      <div className="flex gap-5 border-b-[1px] pb-4">
        <Button label={`N1100`} className={`rounded-md w-[140px]`} />
        <Button label={`N1300`} className={`rounded-md w-[140px]`} />
        <Button label={`N1500`} className={`rounded-md w-[140px]`} />
      </div>
      <h3 className="font-bold">Your max bid</h3>
      <div className="flex items-end gap-3">
        <Input title={`Enter N1100 or more`} className={`w-[350px]`} />
        <Button label={`Place Bid`} className={`rounded-md`} />
      </div>
    </div>
  );
};

export default BidModal;
