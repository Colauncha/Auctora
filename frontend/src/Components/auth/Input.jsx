const Input = ({ title, htmlFor, type, id, className, placeholder,onChange,value }) => {
  return (
    <div className="flex flex-col">
      <label
        className={`text-[13px] lg:text-[15px] text-slate-500 ${className}`}
        htmlFor={htmlFor}
      >
        {title}
      </label>
      <input
        type={type}
        id={id}
        placeholder={placeholder}
        onChange={onChange}
        value={value}
        required
        className={`border-[1px] rounded-md w-full h-[35px]  px-3 ${className}`}
      />
    </div>
  );
};

export default Input;
