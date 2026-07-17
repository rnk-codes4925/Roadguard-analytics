export interface AccidentRecord {
  Accident_Index: string;
  Date: string;
  Year: number;
  Month: number;
  MonthName: string;
  Speed_Limit: number;
  Road_Type: string;
  Urban_or_Rural_Area: 'Urban' | 'Rural';
  Weather_Conditions: string;
  Light_Conditions: 'Day' | 'Dark';
  Road_Surface_Conditions: string;
  Casualties: number;
  Severity: 'Fatal' | 'Serious' | 'Slight';
  District: string;
  Latitude: number;
  Longitude: number;
  Vehicle_Type: string;
}

// Generate realistic mock records to drive the dashboard
export function generateMockRecords(): AccidentRecord[] {
  const records: AccidentRecord[] = [];
  const districts = [
    { name: 'Birmingham', lat: 52.4862, lon: -1.8904, p: 0.25 },
    { name: 'Leeds', lat: 53.8008, lon: -1.5491, p: 0.18 },
    { name: 'Cornwall', lat: 50.2632, lon: -5.0510, p: 0.12 },
    { name: 'Bradford', lat: 53.7960, lon: -1.7594, p: 0.10 },
    { name: 'Sheffield', lat: 53.3811, lon: -1.4701, p: 0.09 },
    { name: 'County Durham', lat: 54.7761, lon: -1.5733, p: 0.07 },
    { name: 'Liverpool', lat: 53.4084, lon: -2.9916, p: 0.06 },
    { name: 'Cheshire East', lat: 53.2291, lon: -2.3168, p: 0.05 },
    { name: 'Manchester', lat: 53.4808, lon: -2.2426, p: 0.05 },
    { name: 'Kirklees', lat: 53.6458, lon: -1.7850, p: 0.03 }
  ];

  const roadTypes = [
    { type: 'Single carriageway', p: 0.70 },
    { type: 'Dual carriageway', p: 0.18 },
    { type: 'Roundabout', p: 0.07 },
    { type: 'One way street', p: 0.03 },
    { type: 'Slip road', p: 0.02 }
  ];

  const weatherTypes = [
    { type: 'Fine no high winds', p: 0.80 },
    { type: 'Raining no high winds', p: 0.14 },
    { type: 'Raining + high winds', p: 0.03 },
    { type: 'Snowing no high winds', p: 0.01 },
    { type: 'Fog or mist', p: 0.02 }
  ];

  const roadSurfaces = [
    { type: 'Dry', p: 0.72 },
    { type: 'Wet or damp', p: 0.23 },
    { type: 'Frost or ice', p: 0.03 },
    { type: 'Snow', p: 0.01 },
    { type: 'Flood', p: 0.01 }
  ];

  const vehicleTypes = [
    { type: 'Car', p: 0.75 },
    { type: 'Bike', p: 0.12 },
    { type: 'Bus', p: 0.05 },
    { type: 'Van', p: 0.05 },
    { type: 'Agricultural', p: 0.01 },
    { type: 'Other', p: 0.02 }
  ];

  const months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];

  // Helper helper to pick based on probability
  const pickWeighted = <T>(items: { type?: string; name?: string; p: number }[]): string => {
    const r = Math.random();
    let sum = 0;
    for (const item of items) {
      sum += item.p;
      if (r <= sum) {
        return (item.type || item.name || '') as string;
      }
    }
    return (items[0].type || items[0].name || '') as string;
  };

  // Seeded-like random generation
  let seed = 42;
  const pseudoRandom = () => {
    const x = Math.sin(seed++) * 10000;
    return x - Math.floor(x);
  };

  // Generate 2500 records to keep it smooth in browser while preserving percentages
  const count = 2500;
  for (let i = 0; i < count; i++) {
    const year = pseudoRandom() > 0.45 ? 2022 : 2021; // ~55% CY, 45% PY
    const monthIdx = Math.floor(pseudoRandom() * 12);
    const day = Math.floor(pseudoRandom() * 28) + 1;
    const dateStr = `${year}-${String(monthIdx + 1).padStart(2, '0')}-${String(day).padStart(2, '0')}`;

    // Severity mapping
    const sevRand = pseudoRandom();
    const severity: 'Fatal' | 'Serious' | 'Slight' = 
      sevRand < 0.02 ? 'Fatal' : sevRand < 0.17 ? 'Serious' : 'Slight';

    const speed = [20, 30, 40, 50, 60, 70][Math.floor(pseudoRandom() * 6)];
    
    // Pick based on probabilities
    const roadType = pickWeighted(roadTypes);
    const urbanRural: 'Urban' | 'Rural' = pseudoRandom() > 0.38 ? 'Urban' : 'Rural';
    const weather = pickWeighted(weatherTypes);
    const light: 'Day' | 'Dark' = pseudoRandom() > 0.26 ? 'Day' : 'Dark';
    const roadSurface = pickWeighted(roadSurfaces);
    
    const districtObj = districts.find(d => d.name === pickWeighted(districts)) || districts[0];
    const jitterLat = (pseudoRandom() - 0.5) * 0.05;
    const jitterLon = (pseudoRandom() - 0.5) * 0.05;

    let casualties = 1;
    if (severity === 'Fatal') {
      casualties = pseudoRandom() > 0.8 ? 2 : 1;
    } else if (severity === 'Serious') {
      casualties = pseudoRandom() > 0.85 ? 3 : pseudoRandom() > 0.7 ? 2 : 1;
    } else {
      casualties = pseudoRandom() > 0.95 ? 2 : 1;
    }

    const vehicle = pickWeighted(vehicleTypes);

    records.push({
      Accident_Index: `ACC${2021000000 + i}`,
      Date: dateStr,
      Year: year,
      Month: monthIdx + 1,
      MonthName: months[monthIdx],
      Speed_Limit: speed,
      Road_Type: roadType,
      Urban_or_Rural_Area: urbanRural,
      Weather_Conditions: weather,
      Light_Conditions: light,
      Road_Surface_Conditions: roadSurface,
      Casualties: casualties,
      Severity: severity,
      District: districtObj.name,
      Latitude: districtObj.lat + jitterLat,
      Longitude: districtObj.lon + jitterLon,
      Vehicle_Type: vehicle
    });
  }

  return records;
}
