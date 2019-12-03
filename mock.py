MOCK_COBRA = {
  "Agent": {
    "Model": "101x",
    "DeviceName": "COBRA 85",
    "MAC": "24:A4:2C:38:D3:85",
    "JSONVer": "2.0",
    "Time": "2019-11-18T23:06:16+01:00",
    "Uptime": 14497,
    "Version": "2.1.0",
    "OemID": "0",
    "VendorID": "0",
    "NumOutputs": 1
  },
  "GlobalMeasure": {
    "Voltage": 241,
    "TotalLoad": 33,
    "TotalEnergy": 20364,
    "OverallPowerFactor": 0.72,
    "Frequency": 50,
    "EnergyStart": "1970-01-01T13:02:08+01:00"
  },
  "Outputs": [
    {
      "ID": 1,
      "Name": "Power output 1",
      "State": 1,
      "Action": 6,
      "Delay": 2000,
      "Current": 191,
      "PowerFactor": 0.72,
      "Energy": 20364,
      "Load": 33
    }
  ]
}

MOCK_4C = {
  "Agent": {
    "Model": "PowerPDU 4C",
    "Version": "3.3.1",
    "JSONVer": "2.1",
    "DeviceName": "myNetio",
    "VendorID": 0,
    "OemID": 0,
    "SerialNumber": "24:A4:2C:39:31:2E",
    "Uptime": 2038097,
    "Time": "2019-11-18T21:57:27+00:00",
    "NumOutputs": 4
  },
  "GlobalMeasure": {
    "Voltage": 240.7,
    "Frequency": 50,
    "TotalCurrent": 0,
    "OverallPowerFactor": 0,
    "TotalLoad": 0,
    "TotalEnergy": 7,
    "EnergyStart": "1970-01-01T01:00:00+01:00"
  },
  "Outputs": [
    {
      "ID": 1,
      "Name": "output_1",
      "State": 1,
      "Action": 6,
      "Delay": 5000,
      "Current": 0,
      "PowerFactor": 1,
      "Load": 0,
      "Energy": 2
    },
    {
      "ID": 2,
      "Name": "output_2",
      "State": 0,
      "Action": 6,
      "Delay": 5000,
      "Current": 0,
      "PowerFactor": 0,
      "Load": 0,
      "Energy": 0
    },
    {
      "ID": 3,
      "Name": "output_3",
      "State": 0,
      "Action": 6,
      "Delay": 5000,
      "Current": 0,
      "PowerFactor": 0,
      "Load": 0,
      "Energy": 0
    },
    {
      "ID": 4,
      "Name": "output_4",
      "State": 0,
      "Action": 6,
      "Delay": 5000,
      "Current": 0,
      "PowerFactor": 0,
      "Load": 0,
      "Energy": 4
    }
  ]
}

MOCK_4ALL = {
  "Agent": {
    "Model": "NETIO 4All",
    "Version": "3.3.1",
    "JSONVer": "2.1",
    "DeviceName": "myNetio",
    "VendorID": 0,
    "OemID": 0,
    "SerialNumber": "24:A4:2C:39:28:1A",
    "Uptime": 388,
    "Time": "2019-12-03T21:17:49+00:00",
    "NumOutputs": 4
  },
  "GlobalMeasure": {
    "Voltage": 238.9,
    "Frequency": 50,
    "TotalCurrent": 0,
    "OverallPowerFactor": 0,
    "TotalLoad": 0,
    "TotalEnergy": 0,
    "EnergyStart": "2019-12-03T21:07:50+00:00"
  },
  "Outputs": [
    {
      "ID": 1,
      "Name": "output_1",
      "State": 0,
      "Action": 6,
      "Delay": 5000,
      "Current": 0,
      "PowerFactor": 0,
      "Load": 0,
      "Energy": 0
    },
    {
      "ID": 2,
      "Name": "output_2",
      "State": 0,
      "Action": 6,
      "Delay": 5000,
      "Current": 0,
      "PowerFactor": 0,
      "Load": 0,
      "Energy": 0
    },
    {
      "ID": 3,
      "Name": "output_3",
      "State": 0,
      "Action": 6,
      "Delay": 5000,
      "Current": 0,
      "PowerFactor": 0,
      "Load": 0,
      "Energy": 0
    },
    {
      "ID": 4,
      "Name": "output_4",
      "State": 0,
      "Action": 6,
      "Delay": 5000,
      "Current": 0,
      "PowerFactor": 0,
      "Load": 0,
      "Energy": 0
    }
  ]
}
