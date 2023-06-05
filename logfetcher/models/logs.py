from enum import Enum
from typing import Any, Optional

from pydantic import BaseModel, Field


class Rank(BaseModel):
    lockedIn: bool
    rankPercent: float
    historicalPercent: float
    todayPercent: float
    rankTotalParses: int
    historicalTotalParses: int
    todayTotalParses: int
    guild: dict
    report: dict
    duration: int
    startTime: int
    amount: float
    bracketData: int
    spec: str
    bestSpec: str
    class_no: int = Field(alias="class")
    affixes: Optional[list[int]]
    medal: Optional[str]
    score: Optional[float]
    leaderboard: Optional[bool]
    faction: bool


class EncounterRankings(BaseModel):
    ranks: Optional[list[Rank]]
    bestAmount: float
    medianPerformance: Optional[float]
    averagePerformance: Optional[float]
    totalKills: int
    fastestKill: int
    difficulty: int
    metric: str
    partition: int
    zone: int


class Character(BaseModel):
    encounterRankings: EncounterRankings


class CharacterData(BaseModel):
    character: Character


class Data(BaseModel):
    characterData: CharacterData


class WarcraftLogs(BaseModel):
    data: Data


class LogInfo(BaseModel):
    rankings: Optional[list[float]]
    name: str


example_log: str = """
{
	"data": {
		"characterData": {
			"character": {
				"encounterRankings": {
					"bestAmount": 130.72699754902,
					"medianPerformance": 80.67355309947537,
					"averagePerformance": 78.96197216300334,
					"totalKills": 7,
					"fastestKill": 1419549,
					"difficulty": 10,
					"metric": "playerscore",
					"partition": 1,
					"zone": 32,
					"ranks": [
						{
							"lockedIn": true,
							"rankPercent": 81.16786693377468,
							"historicalPercent": 81.16786693377468,
							"todayPercent": 78.10816450835405,
							"rankTotalParses": 179998,
							"historicalTotalParses": 179998,
							"todayTotalParses": 204672,
							"guild": {
								"id": null,
								"name": null,
								"faction": null
							},
							"report": {
								"code": "1Rv9BrKgHAGTQ4Wp",
								"startTime": 1677843185345,
								"fightID": 3
							},
							"duration": 1594954,
							"startTime": 1677847568243,
							"amount": 130.72699754902,
							"bracketData": 14,
							"spec": "Guardian",
							"bestSpec": "Guardian",
							"class": 2,
							"affixes": [
								9,
								11,
								12,
								132
							],
							"medal": "silver",
							"score": 130.72699754902,
							"leaderboard": 0,
							"faction": 0
						},
						{
							"lockedIn": true,
							"rankPercent": 86.05338800231135,
							"historicalPercent": 86.05338800231135,
							"todayPercent": 56.24383490557538,
							"rankTotalParses": 39493,
							"historicalTotalParses": 39493,
							"todayTotalParses": 151245,
							"guild": {
								"id": null,
								"name": null,
								"faction": null
							},
							"report": {
								"code": "JHp76CawjN8FKWnP",
								"startTime": 1672564382049,
								"fightID": 6
							},
							"duration": 1620900,
							"startTime": 1672573912058,
							"amount": 116.98767605634,
							"bracketData": 12,
							"spec": "Feral",
							"bestSpec": "Feral",
							"class": 2,
							"affixes": [
								3,
								8,
								10,
								132
							],
							"medal": "silver",
							"score": 116.98767605634,
							"leaderboard": 0,
							"faction": 0
						},
						{
							"lockedIn": true,
							"rankPercent": 89.3369897267072,
							"historicalPercent": 89.3369897267072,
							"todayPercent": 58.5004081771717,
							"rankTotalParses": 22764,
							"historicalTotalParses": 22764,
							"todayTotalParses": 204672,
							"guild": {
								"id": null,
								"name": null,
								"faction": null
							},
							"report": {
								"code": "Yy9cgZtmD1kTRpVC",
								"startTime": 1671294643789,
								"fightID": 14
							},
							"duration": 2584570,
							"startTime": 1671312020219,
							"amount": 106.33233568075,
							"bracketData": 12,
							"spec": "Guardian",
							"bestSpec": "Guardian",
							"class": 2,
							"affixes": [
								6,
								10,
								14,
								132
							],
							"medal": "none",
							"score": 106.33233568075,
							"leaderboard": 0,
							"faction": 0
						},
						{
							"lockedIn": true,
							"rankPercent": 80.67355309947537,
							"historicalPercent": 80.67355309947537,
							"todayPercent": 49.81007204271154,
							"rankTotalParses": 22764,
							"historicalTotalParses": 22764,
							"todayTotalParses": 204672,
							"guild": {
								"id": null,
								"name": null,
								"faction": null
							},
							"report": {
								"code": "Yy9cgZtmD1kTRpVC",
								"startTime": 1671294643789,
								"fightID": 7
							},
							"duration": 2261193,
							"startTime": 1671302518703,
							"amount": 94.230088028169,
							"bracketData": 10,
							"spec": "Guardian",
							"bestSpec": "Guardian",
							"class": 2,
							"affixes": [
								6,
								10,
								14,
								132
							],
							"medal": "none",
							"score": 94.230088028169,
							"leaderboard": 0,
							"faction": 0
						},
						{
							"lockedIn": true,
							"rankPercent": 79.0291524407856,
							"historicalPercent": 79.0291524407856,
							"todayPercent": 45.181078494239465,
							"rankTotalParses": 19159,
							"historicalTotalParses": 19159,
							"todayTotalParses": 204672,
							"guild": {
								"id": null,
								"name": null,
								"faction": null
							},
							"report": {
								"code": "CjYKVQ8Fw7mka1Jg",
								"startTime": 1671220350684,
								"fightID": 4
							},
							"duration": 1658568,
							"startTime": 1671222898664,
							"amount": 87.76661971831,
							"bracketData": 9,
							"spec": "Guardian",
							"bestSpec": "Guardian",
							"class": 2,
							"affixes": [
								6,
								10,
								14
							],
							"medal": "silver",
							"score": 87.76661971831,
							"leaderboard": 0,
							"faction": 0
						},
						{
							"lockedIn": true,
							"rankPercent": 75.45958177973607,
							"historicalPercent": 75.45958177973607,
							"todayPercent": 41.91090233421494,
							"rankTotalParses": 15479,
							"historicalTotalParses": 15479,
							"todayTotalParses": 204672,
							"guild": {
								"id": null,
								"name": null,
								"faction": null
							},
							"report": {
								"code": "13L4apwMmGckbDWF",
								"startTime": 1671130952119,
								"fightID": 5
							},
							"duration": 1584640,
							"startTime": 1671142460908,
							"amount": 83.200469483568,
							"bracketData": 8,
							"spec": "Guardian",
							"bestSpec": "Guardian",
							"class": 2,
							"affixes": [
								6,
								10,
								14
							],
							"medal": "silver",
							"score": 83.200469483568,
							"leaderboard": 0,
							"faction": 0
						},
						{
							"lockedIn": true,
							"rankPercent": 61.01327315823305,
							"historicalPercent": 61.01327315823305,
							"todayPercent": 31.64670964032323,
							"rankTotalParses": 11076,
							"historicalTotalParses": 11076,
							"todayTotalParses": 204672,
							"guild": {
								"id": null,
								"name": null,
								"faction": null
							},
							"report": {
								"code": "Lk2X8Jfb3tWn1KHx",
								"startTime": 1671089962271,
								"fightID": 4
							},
							"duration": 1419549,
							"startTime": 1671096458524,
							"amount": 69.169313380282,
							"bracketData": 6,
							"spec": "Guardian",
							"bestSpec": "Guardian",
							"class": 2,
							"affixes": [
								6,
								10
							],
							"medal": "silver",
							"score": 69.169313380282,
							"leaderboard": 0,
							"faction": 0
						}
					]
				}
			}
		}
	}
}"""
