from src.utils.logger import logger
from typing import Dict, List
import difflib


class DiffService:

    def __init__(self) :
         
        logger.info("Diff Service Initialized")


    def generate_diff(self, original_code: str, improved_code: str) -> Dict:

        """
        Generate simple text diff between original and improved code """

        try:

            # Split the code into lines for comparison
            original_lines= original_code.splitlines()
            improved_lines= improved_code.splitlines()

            # Generate simple unified diff
            diff_lines= list( difflib.unified_diff(
                    
                    original_lines,
                    improved_lines,
                    fromfile='Original',
                    tofile='Improved',
                    lineterm=''
                )
            )

            # Join diff lines into a single string
            diff_text= '\n'.join(diff_lines) if diff_lines else "No changes detected"

            # Count basic changes
            changes_summary= self._count_changes(original_lines, improved_lines)

            logger.info("Sucessfully generated simple diff")


            return{

                "diff_text": diff_text,
                "changes_summary": changes_summary,
                "has_changes": len(diff_lines) > 0,
                "success": True
            } 


        except Exception as e:

            logger.error(f"Error generating diff: {str(e)}")
            
            return{

                "diff_text": "Error",
                "changes_summary": {"lines_added": 0, "lines_removed": 0},
                "has_changes": False,
                "success": False,
                "error": str(e)
            } 


    def _count_changes(self, original_lines: List[str], improved_lines: List[str]) -> Dict:
        """ Count how many lines were added or removed based on the actual diff. """
        diff_lines = list(difflib.unified_diff(
            original_lines,
            improved_lines,
            fromfile='Original',
            tofile='Improved',
            lineterm=''
        ))

        lines_added = 0
        lines_removed = 0

        for line in diff_lines:
            if line.startswith('+++') or line.startswith('---') or line.startswith('@@'):
                continue  # skip diff headers
            elif line.startswith('+'):
                lines_added += 1
            elif line.startswith('-'):
                lines_removed += 1

        return{
            "original_lines": len(original_lines),
            "improved_lines": len(improved_lines),
            "lines_added": lines_added,
            "lines_removed": lines_removed
        }


