
using Newtonsoft.Json;
using System;
namespace GtaCarStateScript
{
    public class CarState
    {
        [JsonProperty("timestamp")]
        public DateTime Timestamp { get; set; } = DateTime.UtcNow;
        [JsonProperty("speed")]
        public float Speed { get; set; }
        [JsonProperty("brake_poner")]
        public float BrakePower { get; set; }
        [JsonProperty("throttle_power")]
        public float ThrottlePower { get; set; }
        [JsonProperty("steering_angle")]
        public float SteeringAngle { get; set; }
        [JsonProperty("is_in_vehicle")]
        public bool IsInVehicle { get; set; } = false;
        [JsonProperty("feature_1")]
        public bool feature_1 { get; set; } = false;
        [JsonProperty("feature_2")]
        public bool feature_2 { get; set; } = false;
        [JsonProperty("feature_3")]
        public bool feature_3 { get; set; } = false;
    }
}