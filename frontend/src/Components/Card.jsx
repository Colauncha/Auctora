const Card = ({
  imgUrl,
  itemName,
  price,
  sellerName,
  bid,
  // bidTimes,
  countDown,
}) => {
  return (
    <div className="flex flex-col relative">
      <img
        src={imgUrl}
        alt=""
        className="w-[160px] h-[161px] rounded-md bg-slate-300 md:w-[285px] md:h-[298px] "
      />
      <div className="w-[171px] h-[65px] flex flex-col md:w-[285px]">
        <h3 className="text-[#9F3247] text-[16px] font-[700] md:text-[20px]">
          {itemName}
        </h3>
        <div className="flex md:gap-2 flex-col md:flex-row">
          <div className="flex items-center gap-2">
            <p className="font-[700] w-[70px] text-[16px] text-[#9F3247]">
              ₦{price}
            </p>
            <p className="text-[12px] text-[#9f3247] flex items-center justify-center">
              {bid} bid(s)
            </p>
          </div>
          <div className="flex gap-2 items-center">
            <span className="flex gap-1 text-[10px] text-slate-400">
              <p>Seller:</p>
              {sellerName}
            </span>
            {/* <p className="text-[12px] text-slate-400">{bidTimes}</p> */}
          </div>
        </div>
        <div className="flex items-center justify-center cursor-pointer hover:bg-[#9f3248] text-[10px] text-[#fff] bg-[#9f324864] px-1 py-2 rounded-md font-bold absolute top-[55%] left-3 lg:top-[70%]">
          <p> Time Left</p>: <span className="ml-1">{countDown}</span>
        </div>
      </div>
    </div>
  );
};

export default Card;
