import { search_glass } from "../Constants";

const Search = ({ className, onClick, img, placeholder }) => {
  return (
    <div
      className={`border-[1px] rounded-2xl w-[700px] h-[36px] flex items-center gap-4 p-2 bg-[#F0F0F0] ${className}`}
    >
      <img
        src={img}
        alt="search_btn"
        className="w-5 h-5 cursor-pointer"
        onClick={onClick}
      />
      <input
        type="text"
        placeholder={placeholder}
        className="w-full h-[20px] rounded-md bg-[#F0F0F0] outline-none"
      />
    </div>
  );
};

export default Search;
