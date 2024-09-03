import NewParking from "./components/NewParking";
import ParkCar from "./components/ParkCar";
import UnparkCar from "./components/UnparkCar";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import Service from "./service";
import ParkingSlot from "./components/ParkingSlot";
import ParkingSlotType from "./types/ParkingSlotType";
import imgUrl from "./assets/OOM_Logo.svg"

function App() {
  const queryClient = useQueryClient();
  const { isLoading, data } = useQuery<ParkingSlotType[]>({
    queryKey: ["parkingSlotsData"],
    queryFn: Service.getAllParkingSlots
  });
  const mutationParkingSystem = useMutation({
    mutationFn: Service.newParkingSystem,
    onSuccess: () =>
      queryClient.invalidateQueries({ queryKey: ["parkingSlotsData"] })
  });
  const mutationParkCar = useMutation({
    mutationFn: Service.parkcar,
    onSuccess: () =>
      queryClient.invalidateQueries({ queryKey: ["parkingSlotsData"] })
  });
  const mutationUnparkCar = useMutation({
    mutationFn: Service.unparkCar,
    onSuccess: () =>
      queryClient.invalidateQueries({ queryKey: ["parkingSlotsData"] })
  });

  return (
    <div className="flex-cols flex h-screen w-full bg-slate-50 text-center">
      <div className="hidden h-full w-2/12 flex-col divide-y divide-slate-400 bg-slate-200 p-4 md:flex">
        <img
          src={imgUrl}
          alt="My Happy SVG"
          className="w-16 self-center pb-4 md:w-20 lg:w-24"
        />
        <div className="grid h-full auto-rows-max grid-cols-1 justify-stretch gap-3 py-5">
          <NewParking onSubmit={mutationParkingSystem.mutate} />
          <ParkCar onSubmit={mutationParkCar.mutate} />
          <UnparkCar
            onSubmit={mutationUnparkCar.mutate}
            isLoading={mutationUnparkCar.isLoading}
            data={mutationUnparkCar.data}
            reset={mutationUnparkCar.reset}
          />
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
