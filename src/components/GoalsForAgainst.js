import React, { useCallback, useState } from 'react'
import axios from 'axios'
import {
  Card,
  CardHeader,
  Box,
  CardContent,
  Button,
  Select,
  InputLabel,
  MenuItem,
  Typography,
  CircularProgress,
} from '@material-ui/core'

const teamOptions = [
  'ANA',
  'ARI',
  'BOS',
  'BUF',
  'CAR',
  'CBJ',
  'CGY',
  'CHI',
  'COL',
  'DAL',
  'DET',
  'EDM',
  'FLA',
  'L.A',
  'MIN',
  'MTL',
  'N.J',
  'NSH',
  'NYI',
  'NYR',
  'OTT',
  'PHI',
  'PIT',
  'S.J',
  'STL',
  'T.B',
  'TOR',
  'VAN',
  'VGK',
  'WPG',
  'WSH',
]

const GoalsForAgainst = () => {
  const [teamOne, setTeamOne] = useState('ANA')
  const [teamTwo, setTeamTwo] = useState('ANA')
  const [results, setResults] = useState()
  const [loading, setLoading] = useState(false)

  const handleClickGo = useCallback(async () => {
    setLoading(true)
    const { data } = await axios.post(
      'http://localhost:5000/goals-for-against',
      {
        team_1: teamOne,
        team_2: teamTwo,
      }
    )

    setResults(data)
    setLoading(false)
  }, [teamOne, teamTwo])

  return (
    <Box py={2}>
      <Card>
        <CardHeader title="Goals For/Against Average" />
        <CardContent>
          <Box mb={2} display="flex" flexDirection="row">
            <Box mr={2}>
              <InputLabel>Team 1</InputLabel>
              <Select
                value={teamOne}
                onChange={(e) => setTeamOne(e.target.value)}
              >
                {teamOptions.map((team) => {
                  return (
                    <MenuItem key={team} value={team}>
                      {team}
                    </MenuItem>
                  )
                })}
              </Select>
            </Box>
            <Box>
              <InputLabel>Team 2</InputLabel>
              <Select
                value={teamTwo}
                onChange={(e) => setTeamTwo(e.target.value)}
              >
                {teamOptions.map((team) => {
                  return (
                    <MenuItem key={team} value={team}>
                      {team}
                    </MenuItem>
                  )
                })}
              </Select>
            </Box>
            {loading && (
              <Box display="flex" flexGrow={1} justifyContent="center">
                <CircularProgress />
              </Box>
            )}
            {results && (
              <Box display="flex" flexDirection="row" mx={2}>
                <Box mx={1}>
                  <Typography variant="h6">Team 1 Avg</Typography>
                  <Typography>{results.team_1}</Typography>
                </Box>
                <Box mx={1}>
                  <Typography variant="h6">Team 2 Avg</Typography>
                  <Typography>{results.team_2}</Typography>
                </Box>
                <Box mx={1}>
                  <Typography variant="h6">Overall Avg</Typography>
                  <Typography>{results.average}</Typography>
                </Box>
              </Box>
            )}
          </Box>
          <Button variant="contained" onClick={handleClickGo}>
            Go
          </Button>
        </CardContent>
      </Card>
    </Box>
  )
}

export default GoalsForAgainst
