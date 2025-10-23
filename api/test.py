import pytest
import json
import provider as pv

@pytest.fixture(scope="module")
def client():
    return pv.setup_client()

@pytest.fixture(scope="module")
def session(client):
    return client._session

def test_statics_temps():
    client = pv.setup_client()
    rs = client._session
    start = "2025-10-15"
    end = "2025-10-17"
    result = pv.obtain_temp_statics(client, rs,"Madrid", start_date=start, end_date=end, above_thr=18, below_thr=16)
    
    data = json.loads(result)
    
    assert "average" in data
    assert "max" in data
    assert "hours_above_threshold" in data
    assert len(data["average_by_day"])>0