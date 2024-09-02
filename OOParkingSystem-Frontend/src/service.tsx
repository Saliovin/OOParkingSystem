import axios from "axios";
import ParkingSlotType from "./types/ParkingSlotType";

const apiClient = axios.create({
  baseURL: import.meta.env.VITE_BACKEND_URL,
  headers: {
    "Content-type": "application/json"
  }
});

const getAllParkingSlots = async () => {
  const response = await apiClient.get<ParkingSlotType[]>("/parking-slots");
  return response.data;
};

// @ts-ignore:next-line
const newParkingSystem = ({ entrypoints, parkingSlots }) => {
  const response = apiClient.post("/new-parking-system", {
    entry_points: entrypoints,
    parking_slots: parkingSlots
  });
  return response;
};

// @ts-ignore:next-line
const parkcar = ({ carId, carSize, entrypointId, startTime }) => {
  const response = apiClient.post("/park-car", {
    car_id: carId,
    car_size: carSize,
    entry_point_id: entrypointId,
    start_time: startTime
  });
  return response;
};

// @ts-ignore:next-line
const unparkCar = ({ carId, exitTime }) => {
  const response = apiClient.post("/unpark-car", {
    car_id: carId,
    exit_time: exitTime
  });
  return response;
};

const Service = {
  getAllParkingSlots,
  newParkingSystem,
  parkcar,
  unparkCar
};

export default Service;
