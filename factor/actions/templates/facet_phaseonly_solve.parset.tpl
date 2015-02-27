Strategy.InputColumn = {{ incol }}
Strategy.UseSolver   = F
Strategy.ChunkSize   = {{ chunksize }}
Strategy.Steps       = [solve, correct]

Step.solve.Model.Sources                = []
Step.solve.Model.Cache.Enable           = T
Step.solve.Model.Phasors.Enable         = F
Step.solve.Model.DirectionalGain.Enable = F
Step.solve.Model.Gain.Enable            = F
Step.solve.Model.TEC.Enable             = T
Step.solve.Model.Rotation.Enable        = F
Step.solve.Model.CommonScalarPhase.Enable = T
Step.solve.Operation                    = SOLVE
Step.solve.Solve.Parms                  = ["CommonScalarPhase:*", "TEC:*"]
Step.solve.Solve.CellSize.Freq          = 0
Step.solve.Solve.CellSize.Time          = {{ timestep }}
Step.solve.Solve.CellChunkSize          = 120
Step.solve.Solve.PropagateSolutions     = T
Step.solve.Solve.Options.MaxIter        = 100
Step.solve.Solve.Options.LMFactor       = 1.0
Step.solve.Solve.Options.BalancedEqs    = F
Step.solve.Solve.Options.UseSVD         = T
Step.solve.Model.Beam.Enable            = F
Step.solve.Solve.UVRange                = [{{ uvrange }}]
Step.solve.Solve.Mode                   = COMPLEX

Step.correct.Model.Sources                 = []
Step.correct.Model.CommonScalarPhase.Enable= T
Step.correct.Model.Cache.Enable            = T
Step.correct.Model.TEC.Enable              = T
Step.correct.Model.DirectionalGain.Enable  = F
Step.correct.Model.Gain.Enable             = F
Step.correct.Model.Phasors.Enable          = F
Step.correct.Operation                     = CORRECT
Step.correct.Output.Column                 = {{ outcol }}
Step.correct.Model.Beam.Enable             = F
Step.correct.Output.WriteCovariance        = F