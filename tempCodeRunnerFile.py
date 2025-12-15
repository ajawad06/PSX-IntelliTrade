
            splits = stock.splits
            
            return splits, None
        except Exception as e:
            return None, str(e)
