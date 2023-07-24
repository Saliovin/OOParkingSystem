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
    { entrypoints: number; parkingSlots: unknown },
    unknown
  >;
};

const NewParking = ({ onSubmit }: Props) => {
  const [entrypoints, setEntrypoints] = useState("3");
  const [parkingSlots, setParkingSlots] = useState("");
  return (
    <Dialog.Root>
      <Dialog.Trigger asChild>
        <button className="rounded-md bg-red-600 px-4 py-3 font-bold text-slate-50 shadow-md hover:bg-red-700">
          New Parking System
        </button>
      </Dialog.Trigger>
      <Dialog.Portal>
        <Dialog.Overlay className="fixed inset-0 bg-slate-600 opacity-25" />
        <Dialog.Content className="fixed left-1/2 top-1/2 w-1/6 min-w-fit -translate-x-1/2 -translate-y-1/2 rounded-md bg-slate-50 p-4 shadow-md">
          <Dialog.Title className="text-lg font-bold">
            Parking System
          </Dialog.Title>
          <Dialog.Description className="my-4 text-slate-500">
            Setup a new parking system
          </Dialog.Description>
          <Input
            label="Entrypoints"
            id="entrypointsinput"
            value={entrypoints}
            setValue={setEntrypoints}
          />
          <Input
            label="Parking Slots"
            id="parkingslotsinput"
            value={parkingSlots}
            setValue={setParkingSlots}
          />
          <div className="mt-2 flex justify-end">
            <Dialog.Close asChild>
              <button
                className="rounded-sm bg-emerald-200 p-2"
                onClick={() =>
                  onSubmit({
                    entrypoints: Number(entrypoints),
                    parkingSlots: JSON.parse(parkingSlots) as unknown
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

export default NewParking;
