import { useState } from "react";
import NewParking from "./components/NewParking";
import ParkCar from "./components/ParkCar";
import UnparkCar from "./components/UnparkCar";
import { useQuery, useQueryClient } from "@tanstack/react-query";
import Service from "./service";
import ParkingSlot from "./components/ParkingSlot";
import ParkingSlotType from "./types/ParkingSlotType";

function App() {
  const { isLoading, isError, data, error } = useQuery<ParkingSlotType[]>({
    queryKey: ["repoData"],
    queryFn: Service.getAllParkingSlots
  });

  return (
    <div className="flex-cols flex h-screen w-full bg-slate-50 text-center">
      <div className="hidden h-full w-2/12 flex-col divide-y divide-slate-400 bg-slate-200 p-4 md:flex">
        <img
          src="src/assets/OOM Logo.svg"
          alt="My Happy SVG"
          className="w-16 self-center pb-4 md:w-20 lg:w-24"
        />
        <div className="grid h-full auto-rows-max grid-cols-1 justify-stretch gap-3 py-5">
          <NewParking onSubmit={Service.newParkingSystem} />
          <ParkCar onSubmit={Service.parkcar} />
          <UnparkCar onSubmit={Service.unparkCar} />
        </div>
        <div className="pt-4">OO Parking System</div>
      </div>

      <div className="m-4 flex w-full items-start gap-3">
        {isLoading
          ? "Loading"
          : data?.map((parkingSlot) => (
              <ParkingSlot
                parkingSlotId={parkingSlot.id}
                carId={parkingSlot.car_id}
                key={parkingSlot.id}
              />
            ))}
      </div>
    </div>
  );
}

export default App;
