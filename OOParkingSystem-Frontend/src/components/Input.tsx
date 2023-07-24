type Props = {
  label: string;
  id: string;
  value: string;
  setValue: React.Dispatch<React.SetStateAction<string>>;
};

const Input = ({ label, id, value, setValue }: Props) => {
  return (
    <fieldset className="mb-2 flex items-center gap-4">
      <label className="w-48 text-right" htmlFor={id}>
        {label}
      </label>
      <input
        className="h-8 w-full rounded-sm border-2 bg-inherit px-2"
        id={id}
        value={value}
        onChange={(e) => setValue(e.target.value)}
      />
    </fieldset>
  );
};

export default Input;
