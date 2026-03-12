package main

import (
	"bufio"
	"math/rand"
	"os"
	"slices"
	"time"
    "strings"
)

const MAZE_TIME   = 16
const MAZE_WIDTH  = 50
const MAZE_HEIGHT = 25

type coord struct {
    x int
    y int
}

func (c coord) Add(o coord) coord {
    return coord { c.x + o.x, c.y + o.y }
}

func (c coord) Sub(o coord) coord {
    return coord { c.x - o.x, c.y - o.y }
}

func filter[T any](s []T, predicate func(T) bool) []T {
	result := make([]T, 0, len(s)) // Pre-allocate for efficiency
	for _, v := range s {
		if predicate(v) {
			result = append(result, v)
		}
	}
	return result
}

type maze map[coord][]coord
func generateMaze() maze {
    DIRS := []coord { { 0, -1 },  { 1, 0 },  { 0, 1 },  { -1, 0 } }

    m := make(map[coord][]coord)
    stack := make([]coord, 0, 128)
    stack = append(stack, coord { 0, 0 })

    for len(stack) > 0 {
        p := stack[len(stack)-1]
        filtered_dirs := filter(DIRS, func(v coord) bool {
            dp := p.Add(v)
            if dp.x < 0 || dp.x >= MAZE_WIDTH || dp.y < 0 || dp.y >= MAZE_HEIGHT { return false }
            return !slices.Contains(m[p], dp) && len(m[dp]) == 0
        })

        if len(filtered_dirs) == 0 { 
            stack = stack[:len(stack)-1]
            continue 
        }


        d := filtered_dirs[rand.Intn(len(filtered_dirs))]
        dp := p.Add(d)

        m[p]  = append(m[p], dp)
        m[dp] = append(m[dp], p)

        stack = append(stack, dp)
    }
    return m
}

func (m maze) display(p coord) string {
    const BUF_WIDTH  = 2 * MAZE_WIDTH  + 1 + 1
    const BUF_HEIGHT = 2 * MAZE_HEIGHT + 1

    var maze_map [BUF_HEIGHT * BUF_WIDTH]rune

    for i := range len(maze_map) {
            if i % BUF_WIDTH == BUF_WIDTH - 1 { maze_map[i] = '\n' } else { maze_map[i] = '#' } 
    }

    for p, vs := range m {
        pr := 2 * p.y + 1
        pc := 2 * p.x + 1
        maze_map[pr * BUF_WIDTH + pc] = ' '
        for _, v := range vs {
            vr := 2 * v.y + 1
            vc := 2 * v.x + 1
            maze_map[vr * BUF_WIDTH + vc] = ' '

            d := v.Sub(p)
            maze_map[(pr + d.y) * BUF_WIDTH + (pc + d.x)] = ' '
        }
    }

    pr := 2 * p.y + 1
    pc := 2 * p.x + 1
    maze_map[pr * BUF_WIDTH + pc] = 'O'

    xr := 2 * (MAZE_HEIGHT - 1) + 1
    xc := 2 * (MAZE_WIDTH  - 1) + 1
    maze_map[xr * BUF_WIDTH + xc] = 'X'

    return string(maze_map[:])
}

func main() {
    p := coord{ 0, 0 }
    m := generateMaze()

    startTime := time.Now()
    endTime := startTime.Add(MAZE_TIME * time.Second)

    reader := bufio.NewReader(os.Stdin)
	writer := bufio.NewWriter(os.Stdout)

    const BUF_WIDTH  = 2 * MAZE_WIDTH  + 1
    const BUF_HEIGHT = 2 * MAZE_HEIGHT + 1

    for time.Now().Before(endTime) {
        disp := m.display(p)
		writer.Write([]byte("Use WASD to move around. Reach the X. Remaining time: " + time.Until(endTime).Round(10 * time.Millisecond).String() + "\n" + disp + "Move: "))
		writer.Flush()

        cmd, _ := reader.ReadString('\n')
        cmd = strings.Trim(cmd, " \t\r\n")

        switch cmd {
        case "q", "Q":
            return;
        case "w", "W": if slices.Contains(m[p], p.Add(coord {0, -1})) {
            p = p.Add(coord {0, -1})
        }

        case "a", "A": if slices.Contains(m[p], p.Add(coord {-1, 0})) {
            p = p.Add(coord {-1, 0})
        }

        case "s", "S": if slices.Contains(m[p], p.Add(coord {0,  1})) {
            p = p.Add(coord {0,  1})
        }

        case "d", "D": if slices.Contains(m[p], p.Add(coord {1,  0})) {
            p = p.Add(coord {1,  0})
        }
        }
        if p.x == MAZE_WIDTH - 1 && p.y == MAZE_HEIGHT - 1 {
            writer.Write([]byte("flag{w7f_15_br34d7h_f1r57_534rch}\n"))
			writer.Flush()
            return
        }
    }
	writer.Write([]byte("Ran out of time!\n"))
	writer.Flush()
}
