import argparse
import sys
from .logger import setup_logger

def main():
    parser = argparse.ArgumentParser(
        description="RAGnarok: The last file converter you'll ever need.",
        prog="ragnarok"
    )
    parser.add_argument("input", help="Path to input file or directory")
    parser.add_argument("-o", "--output", help="Path to output markdown file")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose logging")
    parser.add_argument("--dry-run", action="store_true", help="Run without writing output")
    parser.add_argument("--debug", action="store_true", help="Enable debug mode with detailed traces")
    parser.add_argument("--report", action="store_true", help="Generate a structural JSON confidence report sidecar")

    args = parser.parse_args()

    logger = setup_logger(verbose=args.verbose, debug=args.debug)
    logger.info(f"RAGnarok initialized. Target: {args.input}")

    if args.dry_run:
        logger.info("Dry-run enabled. No files will be written.")

    from ragnarok.orchestrator import Orchestrator
    try:
        orchestrator = Orchestrator(config=vars(args))
        markdown_output, doc_iir = orchestrator.process(args.input)
        
        if not args.dry_run:
            output_path = args.output
            if not output_path:
                import os
                # Default output next to the input file
                base, _ = os.path.splitext(args.input)
                output_path = f"{base}.md"
                
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(markdown_output)
            logger.info(f"Conversion successful. Markdown written to: {output_path}")
            
            if args.report:
                from ragnarok.reporting import Reporter
                import json
                report_path = f"{base}_report.json"
                reporter = Reporter()
                report_data = reporter.generate_report(doc_iir)
                with open(report_path, "w", encoding="utf-8") as rf:
                    json.dump(report_data, rf, indent=2)
                logger.info(f"Confidence report generated at: {report_path}")
                
    except Exception as e:
        logger.error(f"Failed to process document: {e}")
        if args.debug:
            raise
        sys.exit(1)

    logger.debug("Execution finished.")

if __name__ == "__main__":
    main()
