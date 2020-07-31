# -*- coding: utf-8 -*-
import random
import math

import pylab

import BeeAndHive
import FuncOrField
import beetestfunc
import time

if __name__ == "__main__":
    try:
        import psyco

        psyco.full()
    except:
        print("Psyco not found")

    # Включаем интерактивный режим
    pylab.ion()

    # Будем сохранять статистику
    stat = BeeAndHive.statistic()

    # Имя файла для сохранения статистики
    stat_fname = "stat/beestat_%s.txt"

    ###################################################
    ##                     Параметры алгоритма
    ###################################################

    # Класс пчел, который будет использоваться в алгоритме

    beetype = FuncOrField.MapGoodOrBadField
    # beetype = FuncOrField.spherebee
    # beetype = FuncOrField.dejongbee
    # beetype = FuncOrField.goldsteinbee
    # beetype = FuncOrField.rosenbrockbee
    # beetype = FuncOrField.testbee
    # beetype = FuncOrField.funcbee

    # Количество пчел-разведчиков
    scoutbeecount = 300

    # Количество пчел, отправляемых на выбранные, но не лучшие участки
    selectedbeecount = 10

    # Количество пчел, отправляемые на лучшие участки
    bestbeecount = 30

    # Количество выбранных, но не лучших, участков
    selsitescount = 15

    # Количество лучших участков
    bestsitescount = 5

    # Количество запусков алгоритма
    runcount = 100

    # Максимальное количество итераций
    maxiteration = 500

    # Через такое количество итераций без нахождения лучшего решения уменьшим область поиска
    max_func_counter = 10

    # Во столько раз будем уменьшать область поиска
    koeff = beetype.GetRangeKoeff()

    ###################################################
    BestPosition = [0, 0]
    for runnumber in range(runcount):
        currhive = BeeAndHive.Hive(scoutbeecount, selectedbeecount, bestbeecount, \
                                   selsitescount, bestsitescount, \
                                   beetype.GetStartRange(), beetype)

        # Начальное значение целевой функции
        best_func = -1.0e9

        # Количество итераций без улучшения целевой функции
        func_counter = 0

        stat.add(runnumber, currhive)

        for n in range(maxiteration):
            currhive.NextStep()

            stat.add(runnumber, currhive)

            if currhive.bestfitness != best_func:
                # Найдено место, где целевая функция лучше
                best_func = currhive.bestfitness
                func_counter = 0

                # Обновим рисунок роя пчел
                # beetestfunc.plotswarm (currhive, 0, 1)

                # print("\n*** iteration %d / %d" % (runnumber + 1, n))
                # print("Best position: %s" % (str(currhive.bestposition)))
                # print("Best fitness: %f" % currhive.bestfitness)
            else:
                func_counter += 1
                if func_counter == max_func_counter:
                    # Уменьшим размеры участков
                    currhive.range = [currhive.range[m] - koeff[m] for m in range(len(currhive.range))]
                    func_counter = 0

                    # print("\n*** iteration %d / %d (new range)" % (runnumber + 1, n))
                    # print("New range: %s" % (str(currhive.range)))
                    # print("Best position: %s" % (str(currhive.bestposition)))
                    # print("Best fitness: %f" % currhive.bestfitness)
            # if n % 10 == 0:
            #     beetestfunc.plotswarm (currhive, 0, 1)


        if currhive.bestfitness <= FuncOrField.speedlost*2:
            exit(125)
        print(currhive.bestfitness)

        # Сохраним значения целевой функции
        BestPosition = currhive.bestposition
        fname = stat_fname % (("%4.4d" % runnumber) + "_fitness")
        fp = open(fname, "w")
        fp.write(stat.formatfitness(runnumber))
        fp.close()

        # Сохраним значения координат
        fname = stat_fname % (("%4.4d" % runnumber) + "_pos")
        fp = open(fname, "w")
        fp.write(stat.formatpos(runnumber))
        fp.close()

        # Сохраним значения интервалов
        fname = stat_fname % (("%4.4d" % runnumber) + "_range")
        fp = open(fname, "w")
        fp.write(stat.formatrange(runnumber))
        fp.close()

        FuncOrField.f.KillPick(BestPosition)
        beetestfunc.plotstat(stat)
