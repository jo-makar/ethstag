// FIXME https://ethereum.org/en/developers/docs/networking-layer/
//       https://github.com/ethereum/execution-specs/
//       https://github.com/ethereum/consensus-specs
//       https://github.com/ethereum/tests

use clap::Parser;

use std::process::ExitCode;

mod execution;

#[derive(Parser)]
struct Args {
    #[arg(default_value = "sepolia", short, long)]
    network: String,
}

fn main() -> ExitCode {
    let args = Args::parse();

    let network = args.network.as_str();
    if !execution::BOOTNODES.contains_key(network) {
        eprintln!("network {network} bootnodes not found");
        return ExitCode::FAILURE;
    }
    println!("using the {network} network");

    ExitCode::SUCCESS
}
