from model.hero import *
from model.map import Map
from model.parameters import Parameters
from model.state import State
from model.abilites import AbilityType
from model.teams import Teams
import json
import random
import time

game = json.loads(input())
game_map = Map(game)  # карта игрового мира
game_params = Parameters(game)  # параметры игры
game_teams = Teams(game)  # моя команда
target = 0
i = 0

while True:
    try:
        """ Получение состояния игры """
        state = State(input(), game_teams, game_params)

        my_buildings = state.my_buildings()
        my_squads = state.my_squads()
        # сортируем по остаточному пути
        my_squads.sort(key=lambda c: c.way.left, reverse=False)

        enemy_buildings = state.enemy_buildings()
        enemy_squads = state.enemy_squads()

        neutral_buildings = state.neutral_buildings()

        forges_buildings = state.forges_buildings()
        start_t = my_buildings[0].id

        """ Играем за мага """
        if game_teams.my_her.hero_type == HeroType.Mag:
            for my_building in my_buildings:
                sort = game_map.get_nearest_towers(my_building.id, enemy_buildings + neutral_buildings)
                if game_teams.enemy_players_have_hero(2):
                    if (my_building.creeps_count > sort[0].creeps_count) and (((my_building.creeps_count - sort[0].creeps_count) / (my_building.creeps_count / 100)) > 40):
                        print(game_teams.my_her.move(my_building.id, sort[0].id, 0.7))
                else:
                    if  (my_building.creeps_count > sort[0].creeps_count) and (((my_building.creeps_count - sort[0].creeps_count) / (my_building.creeps_count / 100)) > 30):
                        print(game_teams.my_her.move(my_building.id, sort[0].id, 1))
                sort_forges = game_map.get_nearest_towers(my_building.id, forges_buildings)
                if (sort_forges[0].player_color != game_teams.my_her.player_color) and (((my_building.creeps_count - my_building.level.player_max_count) / (my_building.level.player_max_count / 100)) > 70):
                    print(game_teams.my_her.move(my_building.id, sort_forges[0].id, 0.6))
                    if sort_forges[0].player_color == game_teams.my_her.player_color:
                        print(game_teams.my_her.move(my_building.id, sort[0].id, 1))
                if sort[0].creeps_count == 0:
                    print(game_teams.my_her.move(my_building.id, sort[0].id, 1))
            if state.ability_ready(AbilityType.Plague):
                print(game_teams.my_her.plague(enemy_buildings[0].id))
            enemy_buildings.sort(key=lambda c: c.creeps_count, reverse=True)
            if (my_building.creeps_count == 0) and (state.ability_ready(AbilityType.Build_exchange)):
                print(game_teams.my_her.exchange(enemy_buildings[0].id, my_building.id))
           
                       

        

        # Применение абилки ускорение
        if len(my_squads) > 4:
            if state.ability_ready(AbilityType.Speed_up):
                location = game_map.get_squad_center_position(my_squads[2])
                print(game_teams.my_her.speed_up(location))

    except Exception as e:
        print(str(e))
    finally:
        """ Требуется для получения нового состояния игры  """
        print("end")

