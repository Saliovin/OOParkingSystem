import * as Dialog from "@radix-ui/react-dialog";
import { Cross2Icon } from "@radix-ui/react-icons";
import Input from "./Input";
import { useState } from "react";
import { UseMutateFunction } from "@tanstack/react-query";
import { AxiosResponse } from "axios";

type Props = {
  onSubmit: UseMutateFunction<
    AxiosResponse,
    unknown,
    { carId: string; carSize: string; entrypointId: number; startTime: Date },
    unknown
  >;
};

const ParkCar = ({ onSubmit }: Props) => {
  const [carId, setCarId] = useState("");
  const [carSize, setCarSize] = useState("");
  const [entrypoint, setEntrypoint] = useState("");
  const [startDate, setStartDate] = useState("");

  return (
    <Dialog.Root>
      <Dialog.Trigger asChild>
        <button className="rounded-md bg-cyan-300 px-4 py-3 font-bold text-slate-600 shadow-md hover:bg-cyan-400">
          Park Car
        </button>
      </Dialog.Trigger>
      <Dialog.Portal>
        <Dialog.Overlay className="fixed inset-0 bg-slate-600 opacity-25" />
        <Dialog.Content className="fixed left-1/2 top-1/2 w-1/6 min-w-fit -translate-x-1/2 -translate-y-1/2 rounded-md bg-slate-50 p-4 shadow-md">
          <Dialog.Title className="text-lg font-bold">Park Car</Dialog.Title>
          <Dialog.Description className="my-4 text-slate-500">
            Get a parking slot for your car
          </Dialog.Description>
          <Input
            label="Plate Number"
            id="platenumberparkinput"
            value={carId}
            setValue={setCarId}
          />
          <Input
            label="Car Size"
            id="carsizeinput"
            value={carSize}
            setValue={setCarSize}
          />
          <Input
            label="Entrypoint"
            id="entrypointinput"
            value={entrypoint}
            setValue={setEntrypoint}
          />
          <Input
            label="Start Date"
            id="startdateinput"
            value={startDate}
            setValue={setStartDate}
          />
          <div className="mt-2 flex justify-end">
            <Dialog.Close asChild>
              <button
                className="rounded-sm bg-emerald-200 p-2"
                onClick={() =>
                  onSubmit({
                    carId: carId,
                    carSize: carSize,
                    entrypointId: Number(entrypoint),
                    startTime: new Date(startDate)
                  })
                }
              >
                Submit
              </button>
            </Dialog.Close>
          </div>
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

export default ParkCar;
