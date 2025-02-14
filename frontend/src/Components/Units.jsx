import Input from "./auth/Input";

const Units = () => {
  return (
    <div className="lg:w-[300px] flex flex-col gap-8">
      <Input
        title={`Number of units availabley`}
        placeholder={`Availability`}
      />
      <div className="flex flex-col gap-2 w-[150px]">
        <div className="flex justify-between">
          <p className="text-slate-400">Length (mm)</p>
          <Input type={`text`} className={`w-[20px]`} />
        </div>
        <div className="flex justify-between">
          <p className="text-slate-400">Width (mm)</p>
          <Input type={`text`} className={`w-[20px]`} />
        </div>
        <div className="flex justify-between">
          <p className="text-slate-400">height (mm)</p>
          <Input type={`text`} className={`w-[20px]`} />
        </div>
      </div>
      <Input title={`Initial Price`} placeholder={`Product Price`} />
    </div>
  );
};

export default Units;
