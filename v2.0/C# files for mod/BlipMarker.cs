using System;
using System.Collections.Generic;
using System.Linq;
using System.Security.Policy;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using GTA;
using GTA.Math;
using GTA.Native;
using NetMQ;
using NetMQ.Sockets;
using Newtonsoft.Json;

namespace BlipAndMap
{
    public class BlipMarker : Script
    {
        private long ticks = 0;
        private readonly object stateLock = new object();
        PublisherSocket publisher = null;
        private float x = 0.0f;
        private float y = 0.0f;

        public BlipMarker()
        {
            Tick += OnTick;
            KeyDown += OnKeyDown;
        }

        public static (float, float) getPlayerCoords()
        {
            //lock(stateLock)
            //{
                Vector3 pos = Game.Player.Character.Position;

                float x = pos.X;
                float y = pos.Y;

                return (x, y);
            //}
        }

        public (float, float) GetValues()
        {
            float floatValue1 = 3.14f;
            float floatValue2 = 42.0f;

            return (floatValue1, floatValue2);
        }
        public void resetBlip()
        {
            Function.Call(GTA.Native.Hash.SET_WAYPOINT_OFF);
        }
        public void setBlip()
        {
            Function.Call(GTA.Native.Hash.SET_NEW_WAYPOINT, x, y);
        }

        public void getCoords()
        {
            var subscriber = new SubscriberSocket();

            // Connect to the same address that the Python publisher uses
            subscriber.Connect("tcp://127.0.0.1:1880");

            // Subscribe to the topic "coordinates"
            subscriber.Subscribe("coordinates");

            try
            {
                string topic = subscriber.ReceiveFrameString();
                string message = subscriber.ReceiveFrameString();

                // Split the combined topic and message into individual values
                string[] parts = message.Split(',');
                string[] parts1 = parts[0].Split(':');
                string[] parts2 = parts[1].Split(':');

                x = (float) Convert.ToDouble(parts1[1]);
                y = (float) Convert.ToDouble(parts2[1].Remove(parts2[1].Length - 1));
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Error: {ex.Message}");
            }

        }
        public void updateState()
        {
            //lock (stateLock)
            //{
            (float x, float y) = getPlayerCoords();

            //float x = 1.0f;
            //float y = 2.0f;

            if (publisher == null)
                {
                    publisher = new PublisherSocket();
                    publisher.Bind("tcp://127.0.0.1:1810");
                }
                if (publisher != null)
                {
                    var message = new NetMQMessage();
                    message.Append("player_coords");
                    message.Append(JsonConvert.SerializeObject(new { X = x, Y = y }));

                    publisher.SendMultipartMessage(message);
                }
            //}
        }

        public void OnKeyDown(object sender, KeyEventArgs e)
        {
            if (e.KeyCode == Keys.NumPad0)
            {
                try
                {
                    getCoords();
                    setBlip();
                }
                catch (Exception ex)
                {
                    Console.WriteLine(ex.ToString());
                }
            }
            if (e.KeyCode == Keys.NumPad1)
            {
                try
                {
                    resetBlip();
                }
                catch(Exception ex)
                {
                    Console.WriteLine(ex.ToString());
                }
            }
        }

        public void OnTick(object sender, EventArgs e)
        {
            ticks++;
            if(ticks%20 == 0)
            {
                try
                {
                    updateState();
                }
                catch(Exception ex)
                {
                    Console.WriteLine(ex.ToString());
                }
            }
        }
    }
}
