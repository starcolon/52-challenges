module PRQuad.TreeSpec (main,spec) where

import Test.Hspec
import Test.QuickCheck()
import PRQuad.Tree as T
import Prelude hiding (min, max)
import Data.Maybe(fromJust)

main :: IO ()
main = hspec spec

_b_ ::Bound 
_b_ = (-5,-5,7,7)

spec :: Spec
spec = do

  describe "Quadrant" $ do

    it "split quadrants" $ do
      let qs = splitQuadrant _b_
        in qs `shouldBe` [(1,1,7,7), (-5,1,1,7), (-5,-5,1,1), (1,-5,7,1)]

    it "locate quadrant" $ do
      let{i1 = locateQuadrantBound (-4,1) _b_;
          i2 = locateQuadrantBound (3,0) _b_;
          i3 = locateQuadrantBound (1,1) _b_;
          i4 = locateQuadrantBound (4,5) _b_}
        in [i1, i2, i3, i4] `shouldBe` [3,4,1,1]
 
  describe "Basic creation and insertion" $ do

    it "creates sole tree" $ do
      let n = count $ Sole _b_ (2,4)
        in n `shouldBe` 1

