import pytest
import time
from managers.sample_manager import SampleManager
from loguru import logger

def test_create_manager():

    SampleManager.create_manager("sfx", "tests/configurations/smp_ok.json")

    manager = SampleManager.get_manager("sfx")
    assert manager is not None
    assert len(manager.samples.keys()) > 0

def test_unknown_manager():

    with pytest.raises(ValueError) as ex:
        manager = SampleManager.get_manager("nah")

def test_faulty_conf_manager():

    with pytest.raises(ValueError) as ex:
        SampleManager.create_manager("nah", "tests/configurations/smp_nah.json")

    with pytest.raises(ValueError) as ex:
        SampleManager.create_manager("buggy", "tests/configurations/smp_buggy.json")

    with pytest.raises(ValueError) as ex:
        manager = SampleManager("tests/configurations/smp_nah.json")
    
    with pytest.raises(ValueError) as ex:
        manager = SampleManager("tests/configurations/smp_buggy.json")

def test_play_all_samples():

    manager = SampleManager.create_manager("test", "tests/configurations/smp_ok.json")
    assert manager is not None
    assert len(manager.samples.keys()) > 0

    for sample_name, sound in manager.samples.items():
        logger.debug(f"Playing sample {sample_name}")
        sound.play()
        time.sleep(1)

def test_play_sample_loop():

    manager = SampleManager.create_manager("test", "tests/configurations/smp_ok.json")
    assert manager is not None
    assert len(manager.samples.keys()) > 0

    sound = manager.get_sample("engine_max")
    sound.play(loops=100)
    time.sleep(5)
    sound.stop()

def test_play_sample_loop_start_fade():

    manager = SampleManager.create_manager("test", "tests/configurations/smp_ok.json")
    assert manager is not None
    assert len(manager.samples.keys()) > 0

    sound = manager.get_sample("engine_max")
    sound.play(loops=100, fade_start_ms=1500)
    time.sleep(5)
    sound.stop()

def test_play_sample_loop_end_fade():

    manager = SampleManager.create_manager("test", "tests/configurations/smp_ok.json")
    assert manager is not None
    assert len(manager.samples.keys()) > 0

    sound = manager.get_sample("engine_max")
    sound.play(loops=100)
    sound.stop(fadeout_ms=5000)
    time.sleep(3)



    