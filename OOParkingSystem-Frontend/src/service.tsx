import axios from "axios";
import ParkingSlotType from "./types/ParkingSlotType";

const apiClient = axios.create({
  baseURL: "http://localhost:8000",
  headers: {
    "Content-type": "application/json"
  }
});

const getAllParkingSlots = async () => {
  const response = await apiClient.get<ParkingSlotType[]>("/parking-slots");
  return response.data;
};

const newParkingSystem = async ({ entrypoints, parkingSlots }) => {
  const response = await apiClient.post("/new-parking-system", {
    entry_points: entrypoints,
    parking_slots: parkingSlots
  });
  return response.data;
};

const parkcar = async ({ carId, carSize, entrypointId, startTime }) => {
  const response = await apiClient.post("/park-car", {
    car_id: carId,
    car_size: carSize,
    entry_point_id: entrypointId,
    start_time: startTime
  });
  return response.data;
};

const unparkCar = async ({ carId, exitTime }) => {
  const response = await apiClient.post("/unpark-car", {
    car_id: null,
    exit_time: null
  });
  return response.data;
};

const Service = {
  getAllParkingSlots,
  newParkingSystem,
  parkcar,
  unparkCar
};

export default Service;
