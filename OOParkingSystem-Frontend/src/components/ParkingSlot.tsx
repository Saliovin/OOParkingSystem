type Props = {
  parkingSlotId: number;
  carId: string | null;
};

const ParkingSlot = ({ parkingSlotId, carId }: Props) => {
  return (
    <div
      className={`grid w-40 grid-cols-1 rounded-md ${
        carId ? "bg-red-200" : "bg-slate-200"
      } p-2 shadow-md`}
    >
      <text className="font-bold">Slot {parkingSlotId}</text>
      <text>{carId ? `Occupied: ${carId}` : "Unoccupied"}</text>
    </div>
  );
};

export default ParkingSlot;
