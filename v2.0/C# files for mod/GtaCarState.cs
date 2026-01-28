using GTA;
using NetMQ;
using NetMQ.Sockets;
using Newtonsoft.Json;
using System;
using System.Windows.Forms;

namespace GtaCarStateScript
{
    public class GtaCarState : Script
    {
        private readonly object stateLock = new object();

        public GtaCarState()
        {
            Tick += OnTick;
            KeyDown += OnKeyDown;
        }

        private long ticks = 0;
        private CarState currentState = new CarState();

        PublisherSocket publisher = null;

        private void PublishState()
        {
            lock (stateLock)
            {
                if (publisher == null)
                {
                    publisher = new PublisherSocket();
                    publisher.Bind("tcp://127.0.0.1:1900");
                }
                if (publisher != null)
                {
                    publisher
                        .SendMoreFrame("car_state")
                        .SendFrame(JsonConvert.SerializeObject(currentState));
                }
            }
        }

        private void UpdateState()
        {
            lock (stateLock)
            {
                currentState.Timestamp = DateTime.UtcNow;
                Ped playerPed = Game.Player.Character;
                if (playerPed != null)
                {
                    currentState.IsInVehicle = playerPed.IsInVehicle();
                    if (currentState.IsInVehicle)
                    {
                        Vehicle vehicle = playerPed.CurrentVehicle;
                        if (vehicle != null)
                        {
                            currentState.BrakePower = vehicle.BrakePower;
                            currentState.ThrottlePower = vehicle.ThrottlePower;
                            currentState.SteeringAngle = vehicle.SteeringAngle;
                            currentState.Speed = vehicle.Speed;
                        }
                    }
                }
                else
                {
                    currentState.IsInVehicle = false;
                }
            }
        }

        public void OnKeyDown(object sender, KeyEventArgs e)
        {
            if (e.KeyCode == Keys.F10)
            {
                lock (stateLock)
                {
                    currentState.feature_1 = !currentState.feature_1;
                }
            }
            if (e.KeyCode == Keys.F11)
            {
                lock (stateLock)
                {
                    currentState.feature_2 = !currentState.feature_2;
                }
            }
            if (e.KeyCode == Keys.F12)
            {
                lock (stateLock)
                {
                    currentState.feature_3 = !currentState.feature_3;
                }
            }
        }

        public void OnTick(object sender, EventArgs e)
        {
            ticks++;

            try
            {
                UpdateState();
            }
            catch (Exception ex)
            {
                Console.WriteLine(ex);
            }

            try
            {
                if (ticks % 3 == 0)
                {
                    PublishState();
                }
            }
            catch (Exception ex)
            {
                Console.WriteLine(ex);
            }
        }
    }
}