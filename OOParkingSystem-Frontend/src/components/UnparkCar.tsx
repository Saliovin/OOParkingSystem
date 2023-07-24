import * as Dialog from "@radix-ui/react-dialog";
import { Cross2Icon } from "@radix-ui/react-icons";
import Input from "./Input";
import { useEffect, useState } from "react";
import { UseMutateFunction } from "@tanstack/react-query";
import { AxiosResponse } from "axios";

type Props = {
  onSubmit: UseMutateFunction<
    AxiosResponse,
    unknown,
    { carId: string; exitTime: Date },
    unknown
  >;
  isLoading: boolean;
  data: AxiosResponse<number, unknown> | undefined;
  reset: () => void;
};

const UnparkCar = ({ onSubmit, isLoading, data, reset }: Props) => {
  const [carId, setcarId] = useState("");
  const [exitTime, setExitTime] = useState("");
  const [open, setOpen] = useState(false);
  useEffect(() => {
    if (!open) {
      reset();
    }
  }, [open, reset]);

  return (
    <Dialog.Root open={open} onOpenChange={setOpen}>
      <Dialog.Trigger asChild>
        <button className="rounded-md bg-emerald-300 px-4 py-3 font-bold text-slate-600 shadow-md hover:bg-emerald-400">
          Unpark Car
        </button>
      </Dialog.Trigger>
      <Dialog.Portal>
        <Dialog.Overlay className="fixed inset-0 bg-slate-600 opacity-25" />
        <Dialog.Content className="fixed left-1/2 top-1/2 w-1/6 min-w-fit -translate-x-1/2 -translate-y-1/2 rounded-md bg-slate-50 p-4 shadow-md">
          <Dialog.Title className="text-lg font-bold">Unpark Car</Dialog.Title>
          <Dialog.Description className="my-4 text-slate-500">
            Leave the parking slot and get a parking fee
          </Dialog.Description>
          {isLoading ? (
            "Loading"
          ) : data ? (
            `Your parking fee is PHP${data.data}`
          ) : (
            <>
              <Input
                label="Plate Number"
                id="platenumberunparkinput"
                value={carId}
                setValue={setcarId}
              />
              <Input
                label="Exit Time"
                id="exittimeinput"
                value={exitTime}
                setValue={setExitTime}
              />
              <div className="mt-2 flex justify-end">
                <button
                  className="rounded-sm bg-emerald-200 p-2"
                  onClick={() =>
                    onSubmit({
                      carId: carId,
                      exitTime: new Date(exitTime)
                    })
                  }
                >
                  Submit
                </button>
              </div>
            </>
          )}

          <Dialog.Close asChild>
            <button className="absolute right-4 top-4" aria-label="Close">
              <Cross2Icon className="scale-125" />
            </button>
          </Dialog.Close>
        </Dialog.Content>
      </Dialog.Portal>
    </Dialog.Root>
  );
};

export default UnparkCar;
