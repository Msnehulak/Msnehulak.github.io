---
title: Osu jako mp4 prehravac
slug: projects/osu-as-player/wip
lang: en
css: katex
template: project
dont_index: true
---

# Osu jako mp4 prehravac
Projekt Osu jako mp4 prehravac byl stvořen pro převední jakéhokoliv videa na osu beat map. 

Potom co jem videl jedno z tedlech videi:
https://youtube.com/watch?v=wnL0IAYbKwo
https://youtube.com/watch?v=aRRcYVgqWrg
https://youtube.com/watch?v=aUHO_-oj5U4

ze bych rad udelal program ktery prevede video na osu beat map kde jedna nota = 1px 

## Postup

1. Vezmeme video a prevede me ho na true black end white (1/0)

2. resize video ad se vejde na aktualni AR.

{ AR to size calculator }

2.5 prevedeme video na pozadovane fps

{ OD to fps calculator }

3. pokud tam je 1 nahradime to za notu a pokud 0 nechame to prazdne.

4. vytvorime .osz soubor.

## Pridohy 

### .osz generator
Kdyz jsem resil jaky osz generator pouzit nenasel jsou zadny dobry tak jsem nakonec postavil vlasni

## Rovnice
### CS to size
- r = polomer kruhu
- CS = CS

$r = 54,4 - 4,48 \times \text{CS}$

### AR to ms
#### Main
- $T_{\text{celkem}} = T_{\text{preempt}} + W_{50}$

#### Preempt 
- Pro AR < 5: $T_{\text{preempt}} = 1200 + 120 \times (5 - \text{AR}) \text{ [ms]}$
- Pro AR = 5: $T_{\text{preempt}} = 1200 \text{ ms}$
- Pro AR > 5: $T_{\text{preempt}} = 1200 - 150 \times (\text{AR} - 5) \text{ [ms]}$

#### W 50
- $W_{50} = 200 - 10 \times \text{OD} \text{ [ms]}$

#### HD
S modem HD Pouze pouzit t a vynasobit ho 0.7

- $T_{\text{s hd}} = T_{\text{preempt}} \times 0.7$

osu play filed resolution si 512x384

